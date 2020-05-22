# -*- coding: utf-8 -*-
"""
FlaskX
---------------
Flask application template builder.
"""
from setuptools import setup

setup(
    name='FlaskX',
    version='0.1',
    url='https://github.com/greyli/flaskx',
    license='MIT',
    author='Grey Li',
    author_email='withlihui@gmail.com',
    description='',
    long_description=__doc__,
    long_description_content_type='text/markdown',
    platforms='any',
    packages=['flaskx'],
    zip_safe=False,
    include_package_data=True,
    install_requires=[
        'Flask'
    ],
    keywords='flask extension development',
    classifiers=[
        'Development Status :: 1 - Planning',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ]
)