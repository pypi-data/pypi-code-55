import os
import subprocess
from datetime import datetime
from configparser import ConfigParser
from urllib.request import urlopen
from shutil import copyfile, copyfileobj
from pathlib import Path
from setuptools import Command, find_packages
from setuptools.config import ConfigHandler, ConfigOptionsHandler
from setuptools_scm import get_version


def main():
    """ Initialize documentation.
    """
    config = get_config()
    src = str(Path(__file__).parent.joinpath('skeleton'))
    dst = str(_find_root().joinpath(config['docinit']['doc_dir']))
    _copy_tree(src, dst)
    _download_file(config['docinit']['logo_url'], Path(dst).joinpath('_static/logo.png'))
    _download_file(config['docinit']['favicon_url'], Path(dst).joinpath('_static/favicon.ico'))
    print(f'Dcoumentation initialized in {dst}')

def get_config():
    """ Get the configuration.

    Returns:
        dict: The parsed `setup.cfg`.

    """
    path = _find_root(True)
    config = Config(path)
    return  config.config

def set_vars(scope, config=None):
    """ Inject config variables in the given scope.

    Args:
        scope (dict): The global symbol table.
        config (dict): The parsed `setup.cfg`.
    """
    if not config:
        config = get_config()
    reserved = Config.options
    for key, value in config['docinit'].items():
        if key not in reserved:
            scope[key] = value

def setup_keyword(dist, keyword, value):
    """ The callback for the `distutils.setup_keywords` entry point.
    """
    main()

def finalize_distribution(dist):
    """ The callback for the `setuptools.finalize_distribution_options` entry point.
    """
    main()


class DocInitCommand(Command):

    """ The callback for the `distutils.commands` entry point.
    """

    description = 'Initialize documentation'
    user_options = []
    boolean_options = []
    negative_opt = {}

    def __getattr__(self, name):
        pass

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        main()


class Parse():

    """ Parse `setup.cfg` options.
    """

    @classmethod
    def option(cls, value, key='', section=''):
        """ Parse an option

        Args:
            value (str): The option value string to parse.
            key (str):  The option key.
            section (str):  The config section.

        Returns:
            The parsed value.

        """
        value = value.strip(' \r')
        if section == 'options' and key.endswith('_requires') :
            return value
        if section == 'options.extras_require':
            return value
        if value.startswith('file:'):
            return ConfigHandler._parse_file(value)
        if value.startswith('attr:'):
            return ConfigOptionsHandler._parse_attr(value)
        if value in ['find:', 'find_namespace:']:
            return _get_packages()
        if '=' in value:
            return cls._parse_dict(ConfigHandler._parse_dict(value))
        if ',' in value or '\n' in value:
            return cls._parse_list(ConfigHandler._parse_list(value))
        return cls._parse_value(value)

    @classmethod
    def _parse_list(cls, l):
        return [cls._parse_value(v) for v in l]

    @classmethod
    def _parse_dict(cls, d):
        return {k: cls._parse_value(v) for k, v in d.items()}

    @staticmethod
    def _parse_value(v):
        if v.lower() in ('true', '1', 'yes'): return True
        if v.lower() in ('false', '0', 'no'): return False
        if v.lower() == 'none': return None
        for t in (int, float, str):
            try:
                v = t(v)
            except ValueError:
                continue
            else:
                break
        return v


class Config():

    """ Load a `setup.cfg` file, parse its contents, and augment it.

    Args:
        path (pathlib.Path): The full path to `setup.cfg`.

    Attributes:
        options (list): The list of DocInit accepted options.
        config (dict): The fully-parsed `setup.cfg` file.

    """

    options = [
        'doc_dir',
        'name',
        'parent_url',
        'logo_url',
        'favicon_url',
        'version',
        'release',
        'packages',
        'author',
        'copyright',
        'analytics',
        'canonical_url'
    ]

    def __init__(self, path):
        self.config = {
            'metadata': {},
            'options': {},
            'docinit': {},
            'build_sphinx': {},
            'git': Git().info
        }
        parser = ConfigParser()
        parser.read(path)
        for section in parser.sections():
            self.config[section] = {k: Parse.option(v, k, section) for (k, v) in parser.items(section)}
        for option in self.options:
            if option not in self.config['docinit']:
                try:
                    getattr(self, '_set_' + option)()
                except AttributeError:
                    self.config['docinit'][option] = None

    def _set_doc_dir(self):
        self.config['docinit']['doc_dir'] = self._find([
            ('build_sphinx', 'source-dir')
        ], 'doc')

    def _set_name(self):
        self.config['docinit']['name'] = self._find([
            ('build_sphinx', 'project'),
            ('metadata', 'name'),
            ('git', 'name')
        ], 'Project')

    def _set_version(self):
        self.config['docinit']['version'] = self._find([
            ('build_sphinx', 'version'),
            ('metadata', 'version')
        ], _get_version())

    def _set_release(self):
        self.config['docinit']['release'] = self._find([
            ('build_sphinx', 'release')
        ], _get_release())

    def _set_author(self):
        self.config['docinit']['author'] = self._find([
            ('metadata', 'author'),
            ('git', 'author')
        ], 'Anonymous')

    def _set_copyright(self):
        begin_year = self.config['git']['year']
        current_year = str(datetime.now().year)
        author = self.config['docinit']['author']
        if (begin_year is None) or (begin_year == current_year):
            copyright = f'{current_year}, {author}'
        else:
            copyright = f'{begin_year}-{current_year}, {author}'
        self.config['docinit']['copyright'] = self._find([
            ('build_sphinx', 'copyright')
        ], copyright)

    def _set_packages(self):
        self.config['docinit']['packages'] = self._find([
            ('options', 'packages')
        ], _get_packages())

    def _find(self, lookups, default=None):
        for lookup in lookups:
            value = self.config
            for key in lookup:
                try:
                    value = value[key]
                except KeyError:
                    value = None
            if value:
                return value
        return default


class Git():

    """ Retrieve basic information in the current git repository.

    Attributes:
        info (dict): The retrieved information.

    """

    def __init__(self):
        self.info = {
            'year': None,
            'name': None,
            'author': None,
            'email': None
        }
        try:
            commit = self._run("git rev-list --max-parents=0 HEAD")
            info = self._run(f"git show -s --format=%ci|%cn|%ce {commit}").split('|')
            self.info['year'] = info[0][0:4]
            self.info['author'] = info[1]
            self.info['email'] = info[2]
            url = self._run("git config --get remote.origin.url")
            self.info['name'] = os.path.basename(url).split('.git')[0]
        except:
            pass

    def _run(self, command):
        p = subprocess.run(command.split(), capture_output=True)
        return p.stdout.decode().strip()


def _find_root(full=False):
    """ Find the project root directory

    This function works by looking for a `setup.cfg` file into the current directory.
    If none is found, it looks in parent directories until it finds one or reaches the
    filesystem root.

    Args:
        full (bool): If ``True``, the full path, including `setup.cfg` is returned.

    Returns:
        pathlib.Path: The root directory or full path to `setup.cfg`.

    """
    path = Path(os.getcwd())
    while True:
        file = path.joinpath('setup.cfg')
        if file.is_file():
            if full:
                return file
            else:
                return path
        if path == path.parent:
            return False
        path = path.parent

def _get_packages():
    root = _find_root()
    packages = find_packages(str(root))
    dirs = []
    for package in packages:
        if not '.' in package:
            dirs.append(str(root.joinpath(package)))
    return dirs

def _get_version():
    return get_version(
        relative_to=str(_find_root(True)),
        local_scheme='no-local-version',
        fallback_version='0.0.0'
    )

def _get_release():
    return get_version(
        relative_to=str(_find_root(True)),
        local_scheme='node-and-timestamp',
        fallback_version='0.0.0'
    )

def _copy_tree(src, dst):
    if os.path.isdir(src):
        if not os.path.isdir(dst):
            os.makedirs(dst)
        files = os.listdir(src)
        for file in files:
            _copy_tree(os.path.join(src, file), os.path.join(dst, file))
    else:
        # Do not overwrite existing files
        if not os.path.isfile(dst):
            copyfile(src, dst)

def _download_file(url, dst):
    if url is None:
        return
    with urlopen(url) as response:
        with open(dst, 'wb') as file:
            copyfileobj(response, file)
