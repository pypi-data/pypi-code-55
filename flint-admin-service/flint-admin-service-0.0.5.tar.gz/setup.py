from setuptools import setup
import os
import sys

_here = os.path.abspath(os.path.dirname(__file__))

if sys.version_info[0] < 3:
    with open(os.path.join(_here, 'README.md')) as f:
        long_description = f.read()
else:
    with open(os.path.join(_here, 'README.md'), encoding='utf-8') as f:
        long_description = f.read()

version = {}
with open(os.path.join(_here, 'admin_service', 'version.py')) as f:
    exec(f.read(), version)

setup(
    name='flint-admin-service',
    version=version['__version__'],
    description=('flint-admin-service'),
    long_description=long_description,
    author='Gaoxin Dai',
    author_email='daigx1990@gmail.com',
    url='https://github.com/flintdev/flint-admin-service',
    license='Apache License 2.0',
    packages=['admin_service'],
    install_requires=[
        'flask==1.1.2',
        'kubernetes==11.0.0',
    ],
    include_package_data=True,
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache Software License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 3'
    ]
    )
