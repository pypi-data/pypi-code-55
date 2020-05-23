#!/usr/bin/env python3

import re
import shutil
import subprocess
from pathlib import Path
from itertools import chain
from typing import Optional

import click
import logbook
import giturlparse
from dulwich.repo import Repo
from dulwich.errors import NotGitRepository
from unidecode import unidecode
from vistickedword import split_words
from logbook.more import ColorizedStderrHandler
from single_version import get_version


logger = logbook.Logger(__name__, level=logbook.WARNING)
DEFAULT_WORKING_DIR = Path('/tmp/')
__version__ = get_version('derivatecustomer', Path(__file__).parent)


def info(text):
    click.secho(text, fg='bright_blue')


def error(text):
    click.secho(text, fg='red', err=True)


def success(text):
    click.secho(text, fg='green')


def red(text):
    return click.style(text, fg='red')


def magenta(text):
    return click.style(text, fg='magenta')


def cyan(text):
    return click.style(text, fg='cyan')


def make_customer_folder_name(vietnamese_name: str) -> str:
    '''
    Convert "Phúc - Đao Thạnh" to "PhucDaoThanh"
    '''
    non_mark = unidecode(vietnamese_name)
    return re.sub(r'[^a-zA-Z0-9]', '', non_mark)


def replace_file_content_if_needed(filepath: Path, oldstring: str, newstring: str):
    '''Only replace content if the oldstring is found in file.'''
    if not filepath.is_file():
        return
    content = filepath.read_text()
    if oldstring not in content:
        return
    replaced = content.replace(oldstring, newstring)
    filepath.write_text(replaced)
    success(f'Modified file {filepath}')


def add_wait_remote_influxdb(filepath: Path):
    if not filepath.is_file():
        return
    content = filepath.read_text()
    m = re.search(r'wait-influxdb\.sh\s*$', content, re.MULTILINE)
    if not m:
        return
    content = content[:m.start()] + 'wait-influxdb.sh influxdb.agriconnect.vn' + content[m.end():]
    filepath.write_text(content)
    success(f'Add InfluxDB host to {filepath}')


def derivate(repo_url: str, codename: str, farmname: str, server: str, abbr: str) -> Optional[Path]:
    dest = DEFAULT_WORKING_DIR / codename
    original_git = 'git@gitlab.com:agriconnect/plantinghouse-controlview.git'
    original_project_name = 'PlantingHouse'

    info(f'Source folder to modify code: {dest}')
    if not dest.exists():
        info(f'Clone {repo_url} to {dest}')
        subprocess.run(('git', 'clone', repo_url, dest))
    elif dest.is_dir():
        try:
            repo = Repo(dest)
        except NotGitRepository:
            error(f'{dest} exists, but not a Git working copy')
            return None
        rconfig = repo.get_config()
        url = rconfig.get(('remote', 'origin'), 'url')
        if url != repo_url:
            error(f'{dest} is a working copy of some other repo')
            return None
    else:
        error(f'Path "{dest}" is a file. Could you delete it?')
        return None

    original_user = 'debian'
    customer_user = 'web'
    deploy_path = dest / 'Deploy'

    click.echo('-------')
    customer_git = f'git@gitlab.com:agriconnect/customer-deployment/{codename}.git'
    info(f'Replace {original_git} with {customer_git}')
    for f in dest.rglob('*.yml'):
        replace_file_content_if_needed(f, original_git, customer_git)

    click.echo('-------')
    demo_domain = 'demo.agriconnect.vn'
    customer_domain = f'{codename}.{server}.agriconnect.vn'
    info(f'Replace {demo_domain} with {customer_domain}')
    for f in chain(dest.rglob('*.yml'), dest.rglob('*.ini')):
        replace_file_content_if_needed(f, demo_domain, customer_domain)

    click.echo('-------')
    original_src_path = f'/home/{original_user}/{original_project_name}/ControlView'
    customer_folder_name = make_customer_folder_name(farmname)
    customer_src_path = f'/home/{customer_user}/{customer_folder_name}/{codename}'
    info(f'Replace {original_src_path} with {customer_src_path}')
    for f in deploy_path.rglob('*'):
        replace_file_content_if_needed(f, original_src_path, customer_src_path)

    click.echo('-------')
    info(f'Replace {original_user} with {customer_user}')
    for f in chain(deploy_path.glob('*'), dest.glob('*.yml')):
        replace_file_content_if_needed(f, original_user, customer_user)

    click.echo('-------')
    original_src_path = f'/home/{customer_user}/{original_project_name}/demo'
    customer_src_path = f'/home/{customer_user}/{customer_folder_name}/{codename}'
    info(f'Replace {original_src_path} with {customer_src_path}')
    for f in deploy_path.rglob('*'):
        replace_file_content_if_needed(f, original_src_path, customer_src_path)

    click.echo('-------')
    original_src_path = f'/home/{customer_user}/PlantingHouse'
    customer_src_path = f'/home/{customer_user}/{customer_folder_name}'
    info(f'Replace {original_src_path} with {customer_src_path}')
    for f in deploy_path.rglob('*'):
        replace_file_content_if_needed(f, original_src_path, customer_src_path)

    click.echo('-------')
    original_codename = 'plantinghouse'
    info(f'Replace {original_codename} with {codename}')
    for f in chain(deploy_path.rglob('*'), dest.glob('project/*')):
        replace_file_content_if_needed(f, original_codename, codename)
    replace_file_content_if_needed(dest.joinpath('.gitlab-ci.yml'), original_codename, codename)

    click.echo('-------')
    original_python = '/usr/bin/python3'
    customer_python = f'/home/{customer_user}/{customer_folder_name}/venv/bin/python3'
    info(f'Replace {original_python} with {customer_python}')
    for f in deploy_path.rglob('*.service'):
        replace_file_content_if_needed(f, original_python, customer_python)

    click.echo('-------')
    original_gunicorn = '/usr/local/bin/gunicorn'
    customer_gunicorn = f'/home/{customer_user}/{customer_folder_name}/venv/bin/gunicorn'
    info(f'Replace {original_gunicorn} with {customer_gunicorn}')
    for f in deploy_path.rglob('*.service'):
        replace_file_content_if_needed(f, original_gunicorn, customer_gunicorn)

    click.echo('-------')
    unused_services = ('generic-board-startup.service', 'beaglebone-gpio.service', 'influxdb.service')
    info('Delete dependency services {}'.format(', ').join(unused_services))
    for f in deploy_path.rglob('*.service'):
        for s in unused_services:
            replace_file_content_if_needed(f, f' {s}', '')

    click.echo('-------')
    info(f'Rename service prefix ph -> {abbr}')
    for f in deploy_path.rglob('*'):
        replace_file_content_if_needed(f, f'ph-', f'{abbr}-')
        replace_file_content_if_needed(f, f'abbr: ph', f'abbr: {abbr}')

    click.echo('-------')
    info('Rename service files')
    for f in deploy_path.rglob('ph-*'):
        new_name = f.name.replace('ph-', f'{abbr}-')
        new_path = f.parent / new_name
        info(f'Rename {f} file to {new_name}')
        f.rename(new_path)

    click.echo('-------')
    info(f'Replace service title: {original_project_name} -> {farmname}')
    for f in chain(deploy_path.rglob('*.service'), dest.glob('project/*')):
        replace_file_content_if_needed(f, original_project_name, farmname)

    click.echo('-------')
    info('Add influxdb.agriconnect.vn to sytemd service files')
    for f in deploy_path.rglob('*.service'):
        add_wait_remote_influxdb(f)

    return dest


@click.command()
@click.option('-g', '--git-repo', 'repo_url', required=True,
              help='Git repo URL of customer code base (fork of PlantingHouse)')
@click.option('-n', '--farm-name', 'farmname', required=True, help='Farm name. Ex: Phúc Đạo Thạnh')
@click.option('-s', '--server', type=click.Choice(('fa', 'fb'), case_sensitive=False), default='fa', show_default=True)
@click.version_option(__version__)
def main(repo_url, farmname, server):
    repo = giturlparse.parse(repo_url)
    codename = click.prompt('Farm codename (Press Enter to accept default)?', default=repo.name)
    words = codename.split('-')
    words = tuple(chain.from_iterable(split_words(w) for w in words))
    suggested_abbr = ''.join(w[0] for w in words)
    abbr = click.prompt('Please give abbreviate for farm code name', default=suggested_abbr)
    click.echo('You will clone PlantingHouse software for "{}" customer.'.format(red(farmname)))
    click.echo('Codename: {}'.format(magenta(codename)))
    click.echo('Deployed server: {}'.format(cyan(server)))
    click.echo("In server's folder: {}".format(red(make_customer_folder_name(farmname))))
    click.echo('The domain name will be: {}.{}.agriconnect.vn'
               .format(magenta(codename), cyan(server)))
    click.echo('Systemd service will be: {}-controlview.service'.format(click.style(abbr, fg='yellow')))
    click.echo('-------')
    dest = derivate(repo_url, codename, farmname, server, abbr)

    click.echo('')
    message = f'Done!\nThe source code is saved in {dest}. Please come over to commit and push the code.'
    if shutil.which('cowsay'):
        subprocess.run(('cowsay', message))
    else:
        success(message)


if __name__ == '__main__':
    ColorizedStderrHandler().push_application()
    main()
