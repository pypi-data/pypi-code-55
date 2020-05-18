#!/usr/bin/env python3

import setuptools


with open("README.md", "r") as fh:
	long_description = fh.read()


setuptools.setup(
	name="ipo",
	version="0.0.1",
	author="Midgard",
	author_email=None,
	description="Infix piping operator",
	long_description=long_description,
	long_description_content_type="text/markdown",
	url="https://framagit.org/Midgard/ipo",
	packages=setuptools.find_packages(),
	classifiers=[
		"Programming Language :: Python :: 3",
		"License :: OSI Approved :: GNU Lesser General Public License v3 or later (LGPLv3+)",
		"Operating System :: OS Independent",
		"Intended Audience :: Developers",
		"Development Status :: 3 - Alpha",
	],
	python_requires='>=3.6',
)
