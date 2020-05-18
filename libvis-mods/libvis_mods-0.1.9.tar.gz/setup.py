from os import path
from setuptools import setup, find_packages

# read the contents of your README file
this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'README.md'), encoding='utf-8') as f:
        long_description = f.read()

setup(
    name='libvis_mods',
    version='0.1.9',
    license='MIT',

    packages=find_packages(),
    python_requires='>=3.6',

    author = 'Danil Lykov',
    author_email = 'lkvdan@gmail.com',

    include_package_data=True,
    install_requires = ['loguru', 'click', 'libvis'
                       ,'watchdog', 'cookiecutter'],
    setup_requires = ['pytest-runner'],
    tests_require  = ['pytest', 'mock'],
    test_suite='tests',


    entry_points = {
        'console_scripts':['libvis-mods=libvis_mods.cli:cli']
    },

    url='https://github.com/libvis',
    description='cli tool to manage libivs modules',
    long_description=long_description,
    long_description_content_type='text/markdown',
    keywords = ['tools', 'libvis', 'package manager', 'data', 'framework', 'visualization'],

)
