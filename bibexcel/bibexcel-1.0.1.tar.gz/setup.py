# -*- coding: utf-8 -*-
import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name='bibexcel',
    version='1.0.1',
    description='A python executable to get JSON and Excel data from a bibexcel text file',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url='http://github.com/storopoli/bibexcel',
    author='Jose Eduardo Storopoli',
    author_email='thestoropoli@gmail.com',
    license='MIT',
    packages=setuptools.find_packages(),
    install_requires=[
        'pandas',
        'json'
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    zip_safe=False)