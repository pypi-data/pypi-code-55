#!/usr/bin/env python3
# -*- coding:utf-8 -*-

from setuptools import setup

with open("./LongDescription", 'r') as README_FILE:
    long_description = README_FILE.read()

setup(
   name='PathPandem',
   version='1.0',
   description='Simulate Pandemic Pathogen Outbreak',
   license="GPLv3",
   long_description=long_description,
   author='Pradyumna Paranjape',
   author_email='pradyparanjpe@rediffmail.com',
   url="",
   packages=['PathPandem'],  #same as name
   install_requires=['numpy', 'gooey', 'matplotlib'], #external packages as dependencies
   scripts=[
            'PathPandem/spread_simul.py',
           ]
)
