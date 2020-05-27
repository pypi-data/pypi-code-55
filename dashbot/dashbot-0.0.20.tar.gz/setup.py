import pip
import re
import sys
from setuptools import setup, find_packages
from codecs import open
from os import path

from dashbot import version

here = path.abspath(path.dirname(__file__))
 
# Get the long description from the README file
with open(path.join(here, 'README'), encoding='utf-8') as f:
    long_description = f.read()


def parse_version(version_string):
    p = r"""
        ^\s*v?
        (?:
            (?:(?P<epoch>[0-9]+)!)?                         
            (?P<release>[0-9]+(?:\.[0-9]+)*)           
        )?\s*$
    """
    _regex = re.compile(p, re.VERBOSE | re.IGNORECASE)
    match = _regex.search(version_string)
    return tuple(int(i) for i in match.group("release").split("."))


pip_version = parse_version(pip.__version__)
pip_major = pip_version[0]
pip_minor = pip_version[1]

py_major = sys.version_info[0]
py_minor = sys.version_info[1]


install_requires = [
    'requests',
    'dpath',
    'flatten-dict'
]


supports_url_install = pip_major > 18 or (pip_major == 18 and pip_minor >= 1)
rasa_py_compatible = (py_major == 3 and py_minor == 6) or (py_major == 3 and py_minor == 7)


if supports_url_install and rasa_py_compatible:
    install_requires.append(
        'scrubadub @ git+git://github.com/CrisisTextLine/scrubadub.git@master#egg=scrubadub'
    )


setup(
    name='dashbot',
  
    # Versions should comply with PEP440.  For a discussion on single-sourcing
    # the version across setup.py and the project code, see
    # https://packaging.python.org/en/latest/single_source_version.html
    version=version.__version__,
  
    description='Dashbot Python SDK',
    long_description=long_description,
  
    # The project's main homepage.
    url='https://github.com/actionably/dashbotpy',
  
    # Author details
    author='Ryan Mortensen',
    author_email='ryanm@dashbot.io',
  
    # Choose your license
    license='MIT',
  
    classifiers=[
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
        'License :: OSI Approved :: MIT License',
        # Specify the Python versions you support here. In particular, ensure
        # that you indicate whether you support Python 2, Python 3 or both.
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
    ],
  
    # What does your project relate to?
    keywords='dashbot, alexasdk, skill',
  
    packages=find_packages(),
  
    # List run-time dependencies here.  These will be installed by pip when
    # your project is installed. 
    install_requires=install_requires,


)
