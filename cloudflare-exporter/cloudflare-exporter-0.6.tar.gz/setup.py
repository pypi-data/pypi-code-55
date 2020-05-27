#!/usr/bin/env python3

import os
import setuptools


def _read_reqs(relpath):
    fullpath = os.path.join(os.path.dirname(__file__), relpath)
    with open(fullpath) as file:
        return [
            s.strip() for s in file.readlines() if (s.strip() and not s.startswith('#'))
        ]


_REQUIREMENTS_TXT = _read_reqs('requirements.txt')
_INSTALL_REQUIRES = [req for req in _REQUIREMENTS_TXT if "://" not in req]

setuptools.setup(
    name='cloudflare-exporter',
    version='0.6',
    author='Criteo',
    url='https://github.com/criteo/cloudflare-exporter',
    author_email='github@criteo.com',
    install_requires=_INSTALL_REQUIRES,
    tests_require=_read_reqs('tests-requirements.txt'),
    dependency_links=[],
    entry_points={'console_scripts': ['run-app = cloudflare_exporter.exporter:main', ], },
    data_files=[('.', ['requirements.txt', 'tests-requirements.txt'])],
    packages=setuptools.find_packages(),
    python_requires='>=3.6',
)
