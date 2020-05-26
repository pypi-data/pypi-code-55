#!/usr/bin/env python
# coding=utf-8

from setuptools import setup, find_packages

setup(
    name='RasaWS',
    version='1.0.1',
    description='文思海辉基于Rasa的多轮对话安装包',
    author='bradzuo',
    author_email='289126709@qq.com',
    url='https://pypi.org',
    #packages=find_packages(),
    packages=['RasaWSHH'],  #这里是所有代码所在的文件夹名称
    install_requires=['requests'],
)