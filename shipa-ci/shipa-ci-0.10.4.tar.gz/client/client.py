import json
import os
import tarfile
import tempfile
import requests

from gitignore import GitIgnore


CONST_TEST_TOKEN = "test-token"
CONST_TEST_SERVER = "test-server"


class ShipaException(Exception):
    pass


class RepositoryFolder(object):
    IGNORE_FILENAME = '.shipaignore'

    def __init__(self, directory, verbose=False):
        assert directory is not None
        assert verbose is not None

        self.directory = directory
        self.verbose = verbose

        ignore_path = os.path.join(directory, self.IGNORE_FILENAME)
        lines = None
        if os.path.isfile(ignore_path) is True:
            with open(ignore_path, 'r') as f:
                lines = f.readlines()
        self.shipa_ignore = GitIgnore(lines or [])

    def create_tarfile(self):

        os.chdir(self.directory)
        if self.verbose:
            print('Create tar archive:')

        def filter(info):
            if info.name.startswith('./.git'):
                return

            filename = info.name[2:]

            if self.shipa_ignore.match(filename):
                if self.verbose:
                    print('IGNORE: ', filename)
                return

            if self.verbose:
                print('OK', filename)
            return info

        f = tempfile.TemporaryFile(suffix='.tar.gz')
        tar = tarfile.open(fileobj=f, mode="w:gz")
        tar.add(name='.',
                recursive=True,
                filter=filter)
        tar.close()
        f.seek(0)
        return f


def parse_step_interval(step_interval):
    if step_interval.endswith('s'):
        return int(step_interval[:len(step_interval) - 1])
    elif step_interval.endswith('m'):
        return int(step_interval[:len(step_interval) - 1]) * 60
    elif step_interval.endswith('h'):
        return int(step_interval[:len(step_interval) - 1]) * 60 * 60
    elif step_interval == '':
        return 1
    else:
        return step_interval


class ShipaClient(object):

    def __init__(self, server, client, email=None, password=None, token=None, verbose=False):
        self.server = server
        if not server.startswith('http'):
            self.urlbase = 'http://{0}'.format(server)
        else:
            self.urlbase = server

        self.email = email
        self.password = password
        self.token = token
        self.verbose = verbose
        self.http = client

        if token is not None:
            self.headers = {"Authorization": "bearer " + self.token}

    def print_response(self, response):
        if self.verbose:
            print(response.text)
            print(response.status_code)

    def auth(self):
        if self.email is None or self.password is None:
            raise ShipaException('Please, provide email and password')

        url = '{0}/users/{1}/tokens'.format(self.urlbase, self.email)
        params = {'password': self.password}
        headers = {'Content-Type': 'application/x-www-form-urlencoded'}

        try:
            r = self.http.post(url, params=params, headers=headers)

            self.print_response(r)

            if r.status_code != 200:
                raise ShipaException('Invalid token or user/password ({0})'.format(r.text))

            self.token = r.json()['token']
            self.headers = {"Authorization": "bearer " + self.token}

        except requests.ConnectionError:
            raise ShipaException("Shipa server connection error")

    def app_deploy(self, appname, directory='.', steps=1, step_interval='1s', step_weight=300):
        files = None
        try:
            url = '{0}/apps/{1}/deploy'.format(self.urlbase, appname)
            if self.server is not CONST_TEST_SERVER:
                folder = RepositoryFolder(directory, verbose=self.verbose)
                file = folder.create_tarfile()
                files = {'file': file}
            body = {'kind': 'git', 'steps': steps, 'step-interval': parse_step_interval(step_interval),
                    'step-weight': step_weight}
            r = self.http.post(url, files=files, headers=self.headers, data=body)

            self.print_response(r)

            if r.text is None:
                raise ShipaException(r.text)

            ok = any(line.strip() == "OK" for line in r.text.split('\n'))

            if ok is False:
                raise ShipaException(r.text)

        except requests.ConnectionError as e:
            raise ShipaException(e)

    def app_create(self, appname, team, pool, platform=None, description=None, dependency_file=None, tag=None,
                   plan=None,
                   router=None, router_opts=dict()):
        try:
            url = '{0}/apps'.format(self.urlbase)
            opts = dict(router_opt.split('=') for router_opt in router_opts)
            body = {'name': appname, 'platform': platform, 'plan': plan, 'teamOwner': team, 'description': description,
                    'pool': pool, 'router': router, 'dependency_filenames': dependency_file, 'tag': tag,
                    'routeropts': opts}
            r = self.http.post(url, headers=self.headers, data=body)

            self.print_response(r)

            if r.status_code != 201:
                raise ShipaException(r.text)

            out = json.loads(r.text)
            if out['status'] != 'success':
                raise ShipaException(out['status'])

            print('App {0} has been created!'.format(appname))
            print('Use app-info to check the status of the app and its units')
            if out['repository_url'] is not None:
                print('Your repository for {0} project is {1}'.format(appname, out['repository_url']))

        except requests.ConnectionError as e:
            raise ShipaException(e)

    def app_remove(self, appname):
        try:
            url = '{0}/apps/{1}'.format(self.urlbase, appname)
            r = self.http.delete(url, headers=self.headers)

            self.print_response(r)

            if r.status_code != 200:
                raise ShipaException(r.text)

            responses = r.text.split('\n')
            for response in responses:
                if response.find("Message") < 0:
                    continue
                out = json.loads(response)
                print(out['Message'].replace('\n', ''))

        except requests.ConnectionError as e:
            raise ShipaException(e)
        except AttributeError:
            print('Done removing application.')

    def autoscale_check(self):
        try:
            print('running autoscale checks')
            url = '{0}/node/autoscale/run'.format(self.urlbase)
            r = self.http.post(url, headers=self.headers)

            self.print_response(r)

            if r.text is None:
                raise ShipaException(r.text)

            if "Node Autoscaler available only" in r.text:
                raise ShipaException(r.text)

            responses = r.text.split('\n')
            for response in responses:
                if response.find("Message") < 0:
                    continue
                out = json.loads(response)
                print(out['Message'].replace('\n', ''))

        except requests.ConnectionError as e:
            raise ShipaException(e)

    def app_move(self, appname, pool):
        url = '{0}/apps/{1}/move'.format(self.urlbase, appname)

        try:
            body = {'pool': pool}
            r = self.http.post(url, headers=self.headers, data=body)

            self.print_response(r)

            if r.text is None:
                raise ShipaException(r.text)

            ok = any(line.strip() == "OK" for line in r.text.split('\n'))

            if ok is False:
                raise ShipaException(r.text.replace('\n\n', ''))

        except requests.ConnectionError as e:
            raise ShipaException(e)

    def pool_add(self, pool, default=False, public=False, accept_drivers=None, app_quota_limit=None, provisioner=None,
                 plan=None, kubernetes_namespace=None):

        try:
            url = '{0}/pools'.format(self.urlbase)
            body = {'name': pool, 'public': public, 'default': default, 'force': True, 'provisioner': provisioner,
                    'plan': plan, 'kubernetesnamespace': kubernetes_namespace, 'appquotalimit': app_quota_limit,
                    'acceptdriver': accept_drivers}

            r = self.http.post(url, headers=self.headers, data=body)

            self.print_response(r)

            if r.status_code != 201:
                raise ShipaException(r.text)

        except requests.ConnectionError as e:
            raise ShipaException(e)

    def pool_remove(self, pool):

        try:
            url = '{0}/pools/{1}'.format(self.urlbase, pool)
            r = self.http.delete(url, headers=self.headers)

            self.print_response(r)

            if r.status_code != 200:
                raise ShipaException(r.text)

        except requests.ConnectionError as e:
            raise ShipaException(e)

    def pool_update(self, pool, default=False, public=False, accept_drivers=None, app_quota_limit=None, plan=None):
        try:
            url = '{0}/pools/{1}'.format(self.urlbase, pool)
            body = {'public': public, 'default': default, 'force': True, 'plan': plan, 'appquotalimit': app_quota_limit,
                    'acceptdriver': accept_drivers}
            r = self.http.put(url, headers=self.headers, data=body)

            self.print_response(r)

            if r.status_code != 200:
                raise ShipaException(r.text)

        except requests.ConnectionError as e:
            raise ShipaException(e)
