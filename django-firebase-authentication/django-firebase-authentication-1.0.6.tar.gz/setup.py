import os
from setuptools import find_packages, setup

with open(os.path.join(os.path.dirname(__file__), 'README.rst')) as readme:
    README = readme.read()

os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

setup(
    name='django-firebase-authentication',
    version="1.0.6",
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
