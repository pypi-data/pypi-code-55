# -*- coding: utf-8 -*-
import setuptools

with open("README.md", "r",encoding='utf-8') as fh:
  long_description = fh.read()

setuptools.setup(
  name="vec2rec",
  version="0.0.1",
  license='Apache License 2.0',
  packages=['vec2rec'],
  author="carrychang",
  author_email="coolcahng@gmail.com",
  url='http://carrychang.top',
  description="embedding tools for recommend system",
  zip_safe=False,
  include_package_data=True,
  install_requires=['tensorflow==1.12.0', 'keras==2.2.0','numpy==1.16.4']  # 所依赖的包
)