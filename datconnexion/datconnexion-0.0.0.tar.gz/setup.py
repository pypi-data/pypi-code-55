from setuptools import setup, find_packages
from datconnexion import __version__

long_description = ''
with open('./README.md') as f:
    long_description = f.read()

setup(name='datconnexion',
    version=__version__,
    description='A python package for Dat Connexion integrations.',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url='https://github.com/NFI-Industries/datconnexion',
    author='Chris Pryer',
    author_email='christophpryer@gmail.com',
    license='PUBLIC',
    packages=find_packages(),
    zip_safe=False)