#!/usr/bin/env python

"""The setup script."""

from setuptools import setup, find_packages

with open('README.md') as readme_file:
    readme = readme_file.read()

with open('CHANGELOG.md') as history_file:
    history = history_file.read()

requirements_list = [requirement for requirement in open('requirements.txt')]

setup_requirements = ['pytest-runner', ]

test_requirements_list = [requirement.rstrip() for requirement in open('requirements_dev.txt')]

setup(
    author="Breno Silva",
    author_email='brenophp@gmail.com',
    python_requires='>=3.5',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Natural Language :: English',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
    ],
    description="CLI for data science projects",
    entry_points={
        'console_scripts': [
            'romeo=romeo:romeo',
        ],
    },
    install_requires=requirements_list,
    license="GNU General Public License v3",
    long_description=readme + '\n\n' + history,
    long_description_content_type="text/markdown",
    include_package_data=True,
    keywords='romeo',
    name='romeo',
    packages=find_packages(include=['template', 'romeo', 'romeo.*']),
    setup_requires=setup_requirements,
    test_suite='tests',
    tests_require=test_requirements_list,
    url='https://github.com/brendalf/romeo',
    version='0.1.0',
    zip_safe=False,
)
