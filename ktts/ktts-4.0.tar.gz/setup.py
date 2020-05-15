import pathlib
from setuptools import setup
from setuptools import setup, find_packages
# The directory containing this file
HERE = pathlib.Path(__file__).parent

# The text of the README file

# This call to setup() does all the work
setup(
    name="ktts",
    version="4.0",
    description="tts for python",
    long_description="To use ktts install it using pip3 install ktts and run 'from ktts import say' after that type 'say('yourcommand')' in your python Compiler",
    long_description_content_type="text/markdown",
    url="https://github.com/Jeyadevanjd/ktts/releases/",
    author="Jeyadevan",
    author_email="leejack17356@gmail.com",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
    ],
    packages=[""],
    include_package_data=True,
    install_requires=["configparser", "html2text"],
    entry_points={
        "console_scripts": [
            "realpython=reader.__main__:main",
        ]
    },
)
