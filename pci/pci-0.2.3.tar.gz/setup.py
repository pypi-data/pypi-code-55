#!/usr/bin/env python3
# coding=utf-8
from setuptools import setup, find_packages

with open("README.md", "r") as file:
	readme = file.read()

setup(
	name="pci",
	version="0.2.3",
	packages=find_packages(),
	url="https://testpypi.python.org/pypi/pci",
	zip_safe=False,
	description="PCI group estimate",
	long_description=readme,
	long_description_content_type="text/markdown",
	author="zhongj",
	author_email="zhong_jie@foxmail.com",
	license="LICENSE.txt",
	python_requires=">=3.5",
	install_requires=['pandas>=0.23.4',
						'numpy>=1.16.3',
						'folium==0.10.1',
						'geopy==1.20.0'
						],
	dependency_links=["https://pypi.tuna.tsinghua.edu.cn/simple/"],

	classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent"],

	)
