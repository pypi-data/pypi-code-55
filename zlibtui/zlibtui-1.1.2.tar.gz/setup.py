import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

install_requires = [
	'beautifulsoup4',
	'blessed',
	'requests',
]

setuptools.setup(
    name="zlibtui", 
    version="1.1.2",
    author="Jean-Francois To",
    author_email="jeanfrancoisto@hotmail.com",
    description="Terminal user interface for Z-library",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/jfto23/zibtui",
    packages=setuptools.find_packages(),
    install_requires = install_requires,
    entry_points = {
        'console_scripts': ['zlibtui=zlibtui.command_line:main'],
        },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
