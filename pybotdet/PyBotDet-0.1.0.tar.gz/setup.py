#!/usr/bin/env/python3
# -*- coding: utf-8 -*-
import setuptools

setuptools.setup(
    name='PyBotDet',
    version='0.1.0',
    author='zxxml',
    author_email='zxxml@outlook.com',
    packages=setuptools.find_packages(),
    install_requires=['fastai', 'pytorch-pretrained-bert']
)
