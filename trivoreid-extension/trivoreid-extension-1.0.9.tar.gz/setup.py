import os

from setuptools import setup, find_packages

VERSION         = '1.0.9'
DESCRIPTION     = 'Wrapper Extension for TrivoreID SDK API'
AUTHOR          = 'Anastasia Gromova'
AUTHOR_EMAIL    = 'id-client-sdk@trivore.com'
LICENSE         = 'Apache 2.0'

this_directory = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    LONG_DESCRIPTION = f.read()

LONG_DESCRIPTION_CONTENT_TYPE = 'text/markdown'

def check_dependencies():

    install_requires = []

    #try:
    #    import unittest
    #except ImportError:
    #    install_requires.append('unittest')

    try:
        import requests
    except ImportError:
        install_requires.append('requests')

    #try:
    #    import mock
    #except ImportError:
    #    install_requires.append('mock')

    return install_requires

if __name__ == "__main__":

    install_requires = check_dependencies()

    setup(name='trivoreid-extension',
        author=AUTHOR,
        author_email=AUTHOR_EMAIL,
        maintainer=AUTHOR,
        maintainer_email=AUTHOR_EMAIL,
        description=DESCRIPTION,
        long_description=LONG_DESCRIPTION,
        long_description_content_type=LONG_DESCRIPTION_CONTENT_TYPE,
        license=LICENSE,
        version=VERSION,
        install_requires=install_requires,
        packages=find_packages())
