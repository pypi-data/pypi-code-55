import itertools
import json
import logging
import os
import shutil
import threading
import time
import urllib.request
from pathlib import Path

import click
import py
import yaml
from dateutil import tz

import ce_api
from ce_api.rest import ApiException
from ce_cli import constants
from ce_cli.pretty_yaml import save_pretty_yaml


class Spinner(object):
    """
    Shamlessly copied from: https://github.com/click-contrib/click-spinner
    """
    spinner_cycle = itertools.cycle(['-', '/', '|', '\\'])

    def __init__(self, beep=False, disable=False, force=False,
                 stream=click.get_text_stream('stdout')):
        self.disable = disable
        self.beep = beep
        self.force = force
        self.stream = stream
        self.stop_running = None
        self.spin_thread = None

    def start(self):
        if self.disable:
            return
        if self.stream.isatty() or self.force:
            self.stop_running = threading.Event()
            self.spin_thread = threading.Thread(target=self.init_spin)
            self.spin_thread.start()

    def stop(self):
        if self.spin_thread:
            self.stop_running.set()
            self.spin_thread.join()

    def init_spin(self):
        while not self.stop_running.is_set():
            self.stream.write(next(self.spinner_cycle))
            self.stream.flush()
            time.sleep(0.25)
            self.stream.write('\b')
            self.stream.flush()

    def __enter__(self):
        self.start()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.disable:
            return False
        self.stop()
        if self.beep:
            self.stream.write('\7')
            self.stream.flush()
        return False


class Info(dict):
    def __init__(self, *args, **kwargs):
        self.path = py.path.local(
            click.get_app_dir(constants.APP_NAME)).join('info.json')
        super(Info, self).__init__(*args, **kwargs)

    def load(self):
        try:
            self.update(json.loads(self.path.read()))
        except py.error.ENOENT:
            pass

    def save(self):
        self.path.ensure()
        with self.path.open('w') as f:
            f.write(json.dumps(self))


pass_info = click.make_pass_decorator(Info, ensure=True)


def title(text):
    click.echo(click.style(text.upper(), fg='cyan', bold=True, underline=True))


def confirmation(text, *args, **kwargs):
    return click.confirm(click.style(text, fg='yellow'), *args,
                         **kwargs)


def question(text, *args, **kwargs):
    return click.prompt(text=text, *args, **kwargs)


def declare(text):
    click.echo(click.style(text, fg='green'))


def notice(text):
    click.echo(click.style(text, fg='cyan'))


def error(text):
    raise click.ClickException(message=click.style(text, fg='red', bold=True))


def warning(text):
    click.echo(click.style(text, fg='yellow', bold=True))


def search_column(message, schema, cancel_token=constants.CANCEL_TOKEN):
    column = question(message, type=str)

    error_message = 'ERROR: There is no such column as {c}. Possible ' \
                    'selections include {l}. If you want to cancel the ' \
                    'last query, type: {ct}'.format(c=column,
                                                    l=list(schema),
                                                    ct=cancel_token)

    while column not in schema:
        column = question(error_message, type=str)
        if column == cancel_token:
            break
    if column == cancel_token:
        return None
    else:
        return column


def check_login_status(info):
    # TODO: APi call to check the login status?
    if constants.ACTIVE_USER not in info or \
            info[constants.ACTIVE_USER] is None:
        raise click.ClickException(
            "You need to login first.\n"
            "In order to login please use: 'cengine auth login'")


def load_config(path):
    if path is None:
        config = {}
    else:
        with open(path, 'rt', encoding='utf8') as f:
            config = yaml.load(f)

    return config


def save_config(config, path, no_docs):
    # Save the pulled pipeline locally
    if os.path.isdir(path):
        raise Exception('{} is a directory. Please provide a path to a '
                        'file.'.format(path))
    elif os.path.isfile(path):
        if not path.endswith('.yaml'):
            path += '.yaml'
        if confirmation('A file with the same name exists already.'
                        ' Do you want to overwrite?'):
            save_pretty_yaml(config, path, no_docs)
            declare('Config file saved to: {}'.format(path))
    else:
        if not path.endswith('.yaml'):
            path += '.yaml'
        save_pretty_yaml(config, path, no_docs)
        declare('Config file saved to: {}'.format(path))


def assert_exists(item, iterable, error_message='Something failed!'):
    if item not in iterable:
        exception = click.ClickException(click.style(
            error_message, fg='red', bold=True))
        raise exception


def api_client(info):
    active_user = info[constants.ACTIVE_USER]
    config = ce_api.Configuration()
    config.host = constants.API_HOST
    config.access_token = info[active_user][constants.TOKEN]

    return ce_api.ApiClient(config)


def api_call(func, *args, **kwargs):
    try:
        return func(*args, **kwargs)
    except ApiException as e:
        error('{}: {}'.format(e.reason, e.body))
    except Exception as e:
        logging.error(str(e))
        error('There is something wrong going on. Please contact '
              'core@maiot.io to get further information.')


def download_artifact(artifact_json, path='/'):
    """
    This will replace the folder with the files if they already exist
    """
    path = Path(path)
    if artifact_json['name'] == '/':
        full_path = path
    else:
        full_path = path / artifact_json['name']

    if artifact_json['is_dir']:
        # TODO: [LOW] Short term fix for empty files being labelled as dirs
        if len(artifact_json['children']) == 0:
            # turn it into a file
            artifact_json['is_dir'] = False
            with open(full_path, 'wb') as f:
                f.write(b'')
        else:
            os.makedirs(full_path, exist_ok=True)
            for child in artifact_json['children']:
                download_artifact(child, path=full_path)
    else:
        # Download the file from `url` and save it locally under `file_name`:
        url = artifact_json['signed_url']
        with urllib.request.urlopen(url) as response, open(full_path,
                                                           'wb') as out_file:

            shutil.copyfileobj(response, out_file)


def format_date_for_display(dt, format='%Y-%m-%d %H:%M:%S'):
    if dt is None:
        return ''
    local_zone = tz.tzlocal()
    # make sure this is UTC
    dt = dt.replace(tzinfo=tz.tzutc())
    local_time = dt.astimezone(local_zone)
    return local_time.strftime(format)


# TODO: [LOW] Hack for now, should be done in API
def get_workers_cpus_from_env_config(env_config):
    workers = int(env_config['execution']['num_workers'])
    cpus_per_worker = \
        int(env_config['execution']['worker_machine_type'].split('-')[-1])
    return workers, cpus_per_worker


def format_uuid(uuid: str):
    return uuid


def find_closest_uuid(substr: str, options):
    candidates = [x.uuid for x in options if x.uuid.startswith(substr)]
    if len(candidates) == 1:
        return candidates[0]
    elif len(candidates) == 0:
        error('No matching IDs found!')
    error('Too many matching IDs.')
