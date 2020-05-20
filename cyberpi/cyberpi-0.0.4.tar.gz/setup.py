# -*- coding: utf-8 -*
import os
from setuptools import setup

dirs = ['cyberpi']
modules = ['cyberpi']
for path,dir_list,file_list in os.walk("./cyberpi"):
    for dir_name in dir_list:
        if dir_name.find("__")==-1 and dir_name.find("egg")==-1:
            dirs.append((path+"/"+dir_name).replace("/",".").replace("..",""))
    for file_name in file_list:
        if file_name.find(".py")!=-1 and file_name.find("__")==-1 and file_name.find(".pyc")==-1:
            modules.append((path+"."+file_name.replace(".py","")).replace("/",".").replace("..",""))
setup(
    name='cyberpi',
    version='0.0.4',
    author='makeblock',
    author_email='flashindream@gmail.com',
    url='https://makeblock.com',
    description=u'library for cyber-pi',
    packages=dirs,
    py_modules=modules,
    install_requires=['makeblock'],
)