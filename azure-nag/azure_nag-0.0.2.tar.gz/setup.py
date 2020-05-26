"""Distribution instructions for the package."""

import os
from setuptools import setup, find_packages

requirements_files = ['requirements.txt']
install_requires = []


def read_file(rel_path):
    """Read file contents."""
    here = os.path.abspath(os.path.dirname(__file__))
    with open(os.path.join(here, rel_path), 'r') as f_h:
        return f_h.read()


def get_version(rel_path):
    """Retrieve version from passed file."""
    for line in read_file(rel_path).splitlines():
        if line.startswith('__version__'):
            delim = '"' if '"' in line else "'"
            return line.split(delim)[1]
    raise RuntimeError("Unable to find version string.")


for requirements_file in requirements_files:
    with open(requirements_file, 'r') as f:
        install_requires += f.readlines()

long_description = read_file('README.md')

setup(
    name='azure_nag',
    version=get_version('azure_nag/__init__.py'),
    packages=find_packages(exclude=['tests']),
    include_package_data=True,
    install_requires=install_requires,
    url='https://github.com/stelligent/azure-nag',
    license='',
    author='Stelligent',
    author_email='jdoe@host.net',
    description='azure-nag static analysis tool',
    long_description=long_description,
    long_description_content_type="text/markdown",
    python_requires='>=3.7',
    entry_points={
        'console_scripts': [
            'azure-nag=azure_nag.main:main'
        ]
    }
)
