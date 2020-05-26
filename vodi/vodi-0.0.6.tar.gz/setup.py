import os
from setuptools import find_packages
from setuptools import setup

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="vodi", # Replace with your own username
    version="0.0.6",
    author="Andrea Caligiuri",
    author_email="andrea.caligiuri@vodafone.com",
    description="a vodafone digital automation tool",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/pypa/sampleproject",
    packages=find_packages(),
    py_modules=['vodi'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.7',
    install_requires=[
            'click',
            'atlassian-python-api'
        ],
    entry_points='''
        [console_scripts]
        vodi=vodi:cli
    ''',

)
