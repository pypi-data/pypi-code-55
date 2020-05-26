from setuptools import setup
from setuptools.command import install
from os.path import join as _join
from os.path import dirname as _dirname

import re
import sys
import pathlib
import pkg_resources as pk
# get_version and conditional adding of pytest-runner
# are taken from 
# https://github.com/mark-adams/pyjwt/blob/b8cc504ee09b4f6b2ba83a3db95206b305fe136c/setup.py

def get_version(package):
    """
    Return package version as listed in `__version__` in `init.py`.
    """
    with open(_join(package, '__init__.py'), 'rb') as init_py:
        src = init_py.read().decode('utf-8')
        return re.search("__version__ = ['\"]([^'\"]+)['\"]", src).group(1)

version = get_version('hepbasestack')

# parse the requirements.txt file
# FIXME: this might not be the best way
install_requires = []
with pathlib.Path('requirements.txt').open() as requirements_txt:
    for line in requirements_txt.readlines():
        if line.startswith('#'):
            continue
        try:
            req = str([j for j in pk.parse_requirements(line)][0])
        except Exception as e:
            print (f'WARNING: {e} : Can not parse requirement {line}')
            continue
        install_requires.append(req)

#with open(join(os.path.dirname(__file__), 'README.md')) as readme:
with pathlib.Path('README.md').open() as readme:
    long_description = readme.read()

tests_require = [
    'pytest>=3.0.5',
    'pytest-cov',
    'pytest-runner',
]

needs_pytest = set(('pytest', 'test', 'ptr')).intersection(sys.argv)
setup_requires = ['pytest-runner'] if needs_pytest else []
#setup_requires += ["matplotlib>=1.5.0"]

setup(name='hepbasestack',
      version=version,
      python_requires='>=3.6.0',
      description='Collection of tools/snippets useful for working with the python data analysis stack. Provides logging, matplotlibstyles, etc.',
      long_description=long_description,
      author='Achim Stoessl',
      author_email="achim.stoessl@gmail.com",
      url='https://github.com/achim1/hepbasestack',
      download_url=f"https://github.com/achim1/hepbasestack/archive/v{version}.tar.gz",
      install_requires=install_requires,
      setup_requires=setup_requires,
      license="GPL",
      platforms=["Ubuntu 16.04", "Ubuntu 16.10", "SL6.1",
                 "Ubuntu 18.04", "Ubuntu 18.10", "Ubuntu 19.04"],
      classifiers=[
        "License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)",
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Science/Research",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3.5",
        "Topic :: Scientific/Engineering :: Physics"
              ],
      keywords=["logging", "utils",\
                "hep", "particle physics"\
                "helpers", "visualization"],
      tests_require=tests_require,
      packages=['hepbasestack'],
      )
