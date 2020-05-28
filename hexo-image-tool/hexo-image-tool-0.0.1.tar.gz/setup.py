#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
@File  : setup.py.py
@Author: donggangcj
@Date  : 2019/4/1
@Desc  : 
'''

from setuptools import setup  # 这个包没有的可以pip一下

setup(
    name="hexo-image-tool",  # 这里是pip项目发布的名称
    version="0.0.1",  # 版本号，数值大的会优先被pip
    keywords=["pip", "hexo", "COMMAND LINE"],
    description="Hexo image tool ",
    long_description="The tool is aimed to simplify the hexo image operation workflow",
    license="MIT Licence",

    url="https://github.com/donggangcj/ucs.git",  # 项目相关文件地址，一般是github
    author="GangDong",
    author_email="donggangcj@gmail.com",

    py_modules=['app'],
    install_requires=[
        "click",
    ],  # 这个项目需要的第三方库
    entry_points={
        'console_scripts': [
            'hexo-image-sync=app:sync']
    }
)
