import pathlib
from setuptools import setup

# Get README:
HERE = pathlib.Path(__file__).parent
README = (HERE / "README.md").read_text()

# Setup:
setup(
    name='pythondl',
    version='1.1.1',
    description='Download YT videos using this simple tool!',
    long_description=README,
    long_description_content_type="text/markdown",
    author='Calamity34',
    author_email='nick.goloushckin@ya.ru',
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
	"Programming Language :: Python :: 3",
	"Programming Language :: Python :: 3.8"
    ],
    packages=['pythondl'],
    install_requires=['bs4','beautifulsoup4','pytube3','requests'],
    scripts = [
        'scripts/pydownloader'
    ]
)

