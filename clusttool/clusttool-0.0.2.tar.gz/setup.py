import setuptools

with open("README.md", "r") as fh:
	long_description = fh.read()
	
setuptools.setup(
	name="clusttool", 
	version="0.0.2",
	author="Marko Niemelä",
	author_email="marko.nieme@gmail.com",
	description="A clustering toolbox package",
	long_description=long_description,
	long_description_content_type="text/markdown",
	url="https://github.com/markoniem/clustering-toolbox",
	packages=setuptools.find_packages(),
	classifiers=[
		"Programming Language :: Python :: 3",
		"License :: OSI Approved :: MIT License",
		"Operating System :: OS Independent",
	],
	python_requires='>=3.5',
)
