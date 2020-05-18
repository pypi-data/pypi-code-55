#!/usr/bin/env python3

import setuptools


with open("README.md", "r") as fh:
	long_description = fh.read()


setuptools.setup(
	name="ipo",
	version="0.0.2",
	author="Midgard",
	author_email=None,
	description="Infix piping operator",
	long_description=long_description,
	long_description_content_type="text/markdown",

	url="https://framagit.org/Midgard/ipo",
	project_urls={
		"Source": "https://framagit.org/Midgard/ipo",
		"Change log": "https://framagit.org/Midgard/ipo/-/blob/master/CHANGELOG.md",
		"Bug tracker": "https://framagit.org/Midgard/ipo/-/issues",
	},

	classifiers=[
		"Programming Language :: Python :: 3",
		"License :: OSI Approved :: GNU Lesser General Public License v3 or later (LGPLv3+)",
		"Operating System :: OS Independent",
		"Intended Audience :: Developers",
		"Development Status :: 3 - Alpha",
		"Topic :: Software Development :: Libraries :: Python Modules",
	],

	packages=setuptools.find_packages(),
	python_requires='>=3.6',

)
