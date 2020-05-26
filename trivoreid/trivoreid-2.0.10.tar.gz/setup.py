import os
import sys

from setuptools import setup, find_packages

VERSION         = '2.0.10'
DESCRIPTION     = 'Wrapper for TrivoreID SDK'
AUTHOR          = 'Anastasia Gromova'
AUTHOR_EMAIL    = 'id-client-sdk@trivore.com'
LICENSE         = 'Apache 2.0'

this_directory = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    LONG_DESCRIPTION = f.read()

LONG_DESCRIPTION_CONTENT_TYPE = 'text/markdown'

def check_dependencies():
    install_requires = []

    try:
        import requests
    except ImportError:
        install_requires.append('requests')

    return install_requires

if __name__ == "__main__":
    install_requires = check_dependencies()

    setup(name='trivoreid',
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
        setup_requires=install_requires,
        packages=find_packages())
