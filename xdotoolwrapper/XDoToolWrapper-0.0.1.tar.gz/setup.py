import setuptools

setuptools.setup(
	name="XDoToolWrapper",
	version="0.0.1",
	author="7435171",
	author_email="48723247842@protonmail.com",
	description="XDoTool Wrapper",
	url="https://github.com/48723247842/XDoToolWrapper",
	packages=setuptools.find_packages(),
	classifiers=[
		"Programming Language :: Python :: 3",
		"License :: OSI Approved :: MIT License",
		"Operating System :: OS Independent",
	],
	python_requires='>=3.6',
)

install_requires = [
	'time',
	'math' ,
	'subprocess'
]
