#!/usr/bin/env python3

"""The setup script."""

from setuptools import setup, find_packages

with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read()

requirements = ['numpy', 'scipy']

setup_requirements = ['pytest-runner']

test_requirements = ['pytest>=3']

setup(
    author="Jonathon Vandezande",
    author_email='jevandezande@gmail.com',
    python_requires='>=3.7',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
    ],
    description="Package for manipulting and plotting data from a differential scanning calorimeter.",
    entry_points={
        'console_scripts': [
            'calorimeter=calorimeter.cli:main',
        ],
    },
    install_requires=requirements,
    license="MIT license",
    long_description=f'{readme}\n\n{history}',
    include_package_data=True,
    keywords='calorimeter',
    name='calorimeter',
    packages=find_packages(include=['calorimeter', 'calorimeter.*']),
    setup_requires=setup_requirements,
    test_suite='tests',
    tests_require=test_requirements,
    url='https://github.com/jevandezande/calorimeter',
    version='0.2.1',
    zip_safe=False,
)
