from setuptools import setup, find_packages
import re

def get_version():
    with open("k3process/_version.py") as fh:
        verLine = fh.read()
        m = re.match("\s*__version__ *= *[\"']([\d.]+)[\"']", verLine)
        if m:
            return m.group(1)
        else:
            raise RuntimeError("Unable to determine version of the project")

setup(
    name='k3process',
    version=get_version(),
    # packages for distribution are found & included automatically
    packages=find_packages(),
    # for defining other resource files if they need to be included in the installation
    package_data={
        '' : ['*.md']
    },
    
    # Set this is using a MANIFEST.in 
    # include_package_data=True,
    
    # libraries from PyPI that this project depends on
    install_requires=[
        'tblib',
        'pytest',
        'pytest-timeout'
    ],
    entry_points={
        'console_scripts': [
            # a list of strings of format:
            # <command> = <package>:<function>
            'k3process-cli = k3process.main.cli:main'
            # , ...
        ]
    }
)