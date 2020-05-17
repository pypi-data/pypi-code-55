import os
import sys
from setuptools import setup

# to install salesfly type the following command:
#      python setup.py install

path, script = os.path.split(sys.argv[0])
os.chdir(os.path.abspath(path))

with open("DESCRIPTION.rst") as f:
    long_description = f.read()

version_contents = {}
with open(os.path.join('salesfly', 'version.py')) as f:
    exec(f.read(), version_contents)

setup(
    name="salesfly",
    version=version_contents['VERSION'],
    description="Python client for Salesfly API",
    long_description=long_description,
    author="Salesfly",
    author_email="hello@salesfly.com",
    url="http://github.com/salesfly/salesfly-python",
    license="MIT",
    keywords=["salesfly", "api", "geoip", "geolocation", "mail"],
    install_requires=[
        "requests>=2.5.0",
        "jsonschema>=3.1.1",
        "PyJWT>=1.6.1"
    ],
    packages=["salesfly"],
    test_suite="tests",
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Topic :: Software Development :: Libraries :: Python Modules"
    ]
)
