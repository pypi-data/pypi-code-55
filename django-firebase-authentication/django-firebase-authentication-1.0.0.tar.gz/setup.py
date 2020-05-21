import os
from setuptools import find_packages, setup

with open(os.path.join(os.path.dirname(__file__), 'README.rst')) as readme:
    README = readme.read()

os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

if os.environ.get('CI_COMMIT_TAG'):
    version = os.environ['CI_COMMIT_TAG']
else:
    version = os.environ['CI_JOB_ID']

setup(
    name='django-firebase-authentication',
    version=version,
    packages=find_packages(),
    install_requires=[
        'firebase-admin',
        'djangorestframework'
    ],
    include_package_data=True,
    license='BSD License',
    description='A DRF authentication provider for Google Firebase AS.',
    long_description=README,
    author='floydya',
    author_email='xfloydya@gmail.com',
)
