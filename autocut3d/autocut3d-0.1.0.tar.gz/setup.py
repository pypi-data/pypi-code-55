#!/usr/bin/env python

"""The setup script."""

from setuptools import setup, find_packages
import os
with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read()

HERE = os.path.abspath(os.path.dirname(__file__))
setup_reqs = ['Cython', 'numpy']
with open(os.path.join(HERE, 'requirements.txt')) as fp:
    install_reqs = [r.rstrip() for r in fp.readlines()
                    if not r.startswith('#') and not r.startswith('git+')]

setup_requirements = ['pytest-runner', ]

test_requirements = ['pytest>=3', ]

setup(
    author="Edson Cavalcanti Neto",
    author_email='edsoncavalcanti@hotmail.com',
    python_requires='>=3.5',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
    ],
    description="a 3D segmentation algorithm based on cellular automata.",
    install_requires=install_reqs,
    license="MIT license",
    long_description=readme + '\n\n' + history,
    include_package_data=True,
    keywords='autocut3d',
    name='autocut3d',
    packages=find_packages(include=['autocut3d', 'autocut3d.*']),
    setup_requires=setup_requirements,
    test_suite='tests',
    tests_require=test_requirements,
    url='https://github.com/edsoncavalcanti/autocut3d',
    version='0.1.0',
    zip_safe=False,
)
