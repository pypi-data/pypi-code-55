from os.path import abspath, join, dirname
from setuptools import find_packages, setup

with open("README.md", "r") as f:
    long_description = f.read()

setup(
    name="facile-gitlab-trigger",
    version="0.0.4",
    author="Fabio Lima",
    author_email="f46io@icloud.com",
    description="testing ",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://www.facile.it",
    package_dir  = {'': 'facile_trigger_helper'},
    install_requires = [
            "python-gitlab ~= 2.2.0",
            "blessings ~= 1.7",
            "PyYAML ~= 5.3.1",
            "typing ~= 3.7.4.1",
            "pyfiglet ~= 0.8.post1",
            "requests_mock ~=1.7.0",
    ],
    Classfiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "License :: MIT",
        "Operating System  ::  OS Independent",
        "Facile.it New Business help out lib "
    ],
    entry_points = {'console_scripts': ['facile-trigger = facile_trigger_helper.facile_trigger_helper:run_cli']}
)