"""Metadata for the Spreadlinks library."""

import setuptools

__version__ = '0.4.1'

with open('README.md', 'r') as input:
    long_description = input.read()

setuptools.setup(
    name='Spreadlinks',
    version=__version__,
    author='Damian Cugley',
    author_email='pdc@alleged.org.uk',
    description='A Django app for serving libraries of links from spreadsheets.',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/pdc/spreadlinks',
    packages=setuptools.find_packages(),
    include_package_data=True,
    package_data={
        'spreadlinks': [
            'static/style/*',
            'templates/jeremyday/*',
            'templates/spreadlinks/*',
        ]
    },
    install_requires=[
        'Markdown',
        'Django',
    ],
    classifiers=(
        'Development Status :: 3 - Alpha',
        'Programming Language :: Python :: 3',
        'Framework :: Django :: 2.0',
        'Framework :: Django :: 1.11',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
    ),
)
