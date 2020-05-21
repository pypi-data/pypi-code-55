import setuptools
import sys
import tclib
with open("README.md", "r") as fh:
	long_description = fh.read()

setuptools.setup(
	name="tclib",
	version=tclib.VERSION,
	author="Tianyi Chen",
	author_email="",
	description="Personal library",
	long_description=long_description,
	long_description_content_type="text/markdown",
	url="https://github.com/TianyiChen/tclib",
	packages=setuptools.find_packages(),
	install_requires=[
		'requests'
	],
	classifiers=[
		"Programming Language :: Python :: 3",
		"License :: OSI Approved :: MIT License",
		"Operating System :: POSIX :: Linux",
	],
)
