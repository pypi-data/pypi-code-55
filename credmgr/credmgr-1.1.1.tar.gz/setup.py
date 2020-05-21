from os import path
import re

from setuptools import find_packages, setup


projectName = 'credmgr'

root = path.abspath(path.dirname(__file__))

with open(path.join(root, projectName, "const.py")) as f:
    __version__ = re.search(r"__version__ = '(.+)'", f.read()).group(1)

with open(path.join(root, "README.rst")) as f:
    longDescription = f.read()

requires = ['setuptools', 'python-dateutil', 'requests', 'praw', 'prawcore', 'requests_toolbelt']
testsRequires = [
    'coverage',
    'pytest',
    'betamax',
    'betamax_serializers',
    'sphinx',
    'pytest-mock',
    'pytest-xdist',
    'pytest-cov',
    'mock',
    'sphinx_rtd_theme'
]
extras = {
    'test': testsRequires,
}

setup(
    name=projectName,
    author='Lil_SpazJoekp',
    author_email='spaz@jesassn.org',
    license='Proprietary',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Operating System :: OS Independent',
        'License :: Other/Proprietary License'
    ],
    python_requires='>=3.6',
    description='Credential Manager API Client',
    include_package_data=True,
    install_requires=requires,
    long_description=longDescription,
    packages=find_packages(exclude=['tests', 'tests.*']),
    test_suite='tests',
    tests_require=testsRequires,
    extras_require=extras,
    url='https://credmgr.jesassn.org',
    version=__version__
)