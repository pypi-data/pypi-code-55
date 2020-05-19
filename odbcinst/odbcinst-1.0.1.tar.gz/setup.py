import os
import re

import setuptools

v = open(os.path.join(os.path.dirname(__file__), 'odbcinst', '__init__.py'))
VERSION = re.compile(r".*__version__ = '(.*?)'", re.S).match(v.read()).group(1)
v.close()

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="odbcinst",
    version=VERSION,
    author="Gord Thompson",
    author_email="gord@gordthompson.com",
    license='MIT',
    description="return output from unixODBC `odbcinst` command",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/gordthompson/odbcinst",
    packages=setuptools.find_packages(),
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: Unix',
    ],
    keywords='unixODBC',
)
