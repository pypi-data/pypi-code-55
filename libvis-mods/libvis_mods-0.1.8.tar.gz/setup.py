from os import path
from setuptools import setup, find_packages

# read the contents of your README file
this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'README.md'), encoding='utf-8') as f:
        long_description = f.read()

setup(
    name='libvis_mods',
    version='0.1.8',
    license='MIT',

    packages=find_packages(),
    python_requires='>=3.6',

    author = 'Danil Lykov',
    author_email = 'lkvdan@gmail.com',

    install_requires = ['loguru', 'click', 'libvis'
                       ,'watchdog', 'cookiecutter'],
    setup_requires = ['pytest-runner'],
    tests_require  = ['pytest'],
    include_package_data=True,
    keywords = ['tools', 'libvis', 'package manager', 'data', 'framework', 'visualization'],

    entry_points = {
        'console_scripts':['libvis-mods=libvis_mods.cli:cli']
    },

    long_description=long_description,
    long_description_content_type='text/markdown',

    test_suite='tests',
)
