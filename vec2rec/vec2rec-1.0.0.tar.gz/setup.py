# -*- coding: utf-8 -*-
import setuptools

 

setuptools.setup(
  name="vec2rec",
  version="1.0.0",
  license='MIT',
  packages=['vec2rec'],
  author="carrychang",
  author_email="coolcahng@gmail.com",
  url='http://carrychang.top',
  include_package_data=True,
  description='An embedding tools for recommend system',
  long_description = 'An embedding tools for recommend system',
  install_requires=['tensorflow==1.12.0', 
  					'keras==2.2.0',
  					'numpy==1.16.4'
  					],
   keywords = "rec embedding vec ml",
   zip_safe= True,
)