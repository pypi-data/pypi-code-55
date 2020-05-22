#!/usr/bin/env python
# encoding: utf-8
# -*- coding: utf-8 -*-

try:
  from setuptools import setup, find_packages, Command
except ImportError:
  from distutils.core import setup, find_packages, Command
finally:
  import os
  import sys
  os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir))) # allow setup.py to be run from any path
  HERE = os.path.abspath(os.path.dirname(__file__))

  def call_(cmd, show_stdout=True, shell=False):
    """Execute *cmd* and return True on success."""
    from subprocess import call
    if show_stdout:
      rc = call(cmd, shell=shell)
    else:
      with open(os.devnull, 'w') as n:
        rc = call(cmd, shell=shell, stdout=n)
    return rc == 0


  def read_file(filename, mode='r', encoding='utf-8'):
    try:
      from io import open
    except ImportError:
      pass
    finally:
      with open(os.path.join(HERE, filename), mode, encoding=encoding) as f:
        return f.read()
  def load_requirements(filename='base', folder='requirements', file_ext='.txt'):
    """Load requirements from a pip requirements file"""
    _ = []
    if not filename.endswith(file_ext):
      filename = f'{filename}{file_ext}'
    for __ in read_file(f'{folder}/{filename}').splitlines():
      if __:
        if __[:3].lower() == '-r ':
          _ += load_requirements(__[3:])
        elif __[:3].lower() == '-e ' or __[0] == '#':
          pass
        else:
          _.append(__)
    return _
  def get_metadata(package_name):
    _ = {}
    exec(read_file(f'{package_name}/__version__.py'), _)
    return _
  def get_readme(filename='README.md'):
    try:
      import pypandoc
    except(IOError, ImportError):
      try:
        return read_file(filename)
      except FileNotFoundError:
        pass
    else:
      return pypandoc.convert(filename, 'rst').replace('\r', '')
  _ = get_metadata('boolify')
  NAME, AUTHOR, AUTHOR_EMAIL, DESCRIPTION, LICENSE, URL, VERSION = _['__package_name__'], _['__author__'], _['__author_email__'], _['__description__'], _['__license__'], _['__url__'], _['__version__']
  class UploadCommand(Command):
    """Support setup.py upload."""
    description = __doc__ or 'Build and publish the package.'
    user_options = []

    @staticmethod
    def recursive_delete(path):
      from shutil import rmtree
      try:
        rmtree(os.path.join(HERE, path))
      except OSError:
        pass
    @staticmethod
    def confirm(msg):
      """ask a yes/no question, return result"""
      if not sys.stdout.isatty():
        return False
      reply = input(f'\n{msg} [Y/N]:')
      return reply and reply[0].lower() == 'y'
    @staticmethod
    def status_msgs(*msgs):
      print('*' * 75)
      for msg in msgs:
        print(msg)
      print('*' * 75)
    @staticmethod
    def status(msg):
      """Prints things in bold."""
      print(f'\033[1m{msg}\033[0m')
    def initialize_options(self):
      try:
        import colorama
      except ImportError:
        pass
      else:
        colorama.init(convert=True)
    def finalize_options(self):
        pass
    def run(self):
      self.status('Removing previous builds…')
      self.recursive_delete('dist')

      self.status('Updating Pip, SetupTools, Twine and Wheel…')
      call_('pip install --upgrade pip setuptools twine wheel')

      self.status('Building Source and Wheel (universal) distribution…')
      call_('{PATH} setup.py sdist bdist_wheel --universal'.format(PATH=sys.executable))

      self.status('Uploading the {NAME} package to PyPI via Twine…'.format(NAME=NAME.capitalize()))
      call_('twine upload dist/*')

      if self.confirm('Push tags'):
        self.status('Pushing git tags…')
        call_('git tag {VERSION}'.format(VERSION=VERSION))
        call_('git push --tags')
      if self.confirm('Clear?'): #rm -r dist build *.egg-info
        self.recursive_delete('dist')
        self.recursive_delete('build')
        self.recursive_delete('{NAME}.egg-info'.format(NAME=NAME))
      sys.exit()
  setup(
    author=AUTHOR,
    author_email=AUTHOR_EMAIL,
    cmdclass={ 'upload': UploadCommand }, #$ setup.py upload support.
    classifiers=[
      'Development Status :: 4 - Beta',
      'Intended Audience :: Developers',
      'License :: OSI Approved :: MIT License',
      'Natural Language :: English',
      'Operating System :: OS Independent',
      'Programming Language :: Python',
      'Programming Language :: Python :: 3',
      'Programming Language :: Python :: 3.6',
      'Programming Language :: Python :: 3.7',
      'Programming Language :: Python :: 3.8',
      'Programming Language :: Python :: Implementation :: CPython',
      'Topic :: Software Development',
      'Topic :: Software Development :: Libraries',
      'Topic :: Software Development :: Libraries :: Python Modules',
      'Topic :: Utilities'
    ],
    description=DESCRIPTION,
    download_url=f'{URL}/archive/{VERSION}.tar.gz',
    extras_require={
      'dev': load_requirements('dev'),
      'docs': load_requirements('docs'),
    },
    keywords=['boolify', 'bool', 'boolean', 'convert', 'open-source', 'library', 'python', 'python3', 'python-3'],
    include_package_data=True,
    install_requires=load_requirements(),
    license=LICENSE,
    long_description=get_readme(),
    long_description_content_type='text/markdown; charset=UTF-8; variant=GFM',
    maintainer=AUTHOR,
    maintainer_email=AUTHOR_EMAIL,
    name=NAME,
    packages=find_packages(exclude=['.git', 'docs', 'tests*', 'examples', 'examples.py', '.gitignore', '.github', '.gitattributes', 'README.md']),
    platforms = 'any',
    python_requires='>=3.6.*',
    setup_requires=load_requirements('base'),
    tests_require=load_requirements('dev'),
    version=VERSION,
    url=URL,
    zip_safe=False,
    project_urls={
      'Discord: Support Server': 'https://discord.gg/XkydRPS',
      'Github: Issues': f'{URL}/issues',
      'Say Thanks!': 'https://saythanks.io/to/luissilva1044894',
    },
  )
