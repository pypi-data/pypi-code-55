"""Setup script for ArduinoPythonSerialRpc"""

import os.path

from setuptools import setup

HERE = os.path.abspath(os.path.dirname(__file__))

with open(os.path.join(HERE, "README.md")) as fid:
    README = fid.read()

setup(
    name="arduinopythonserialrpc",
    version="1.0.0",
    description="Python side of a serial communication library with Arduino Card",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/Mauxilium/ArduinoPythonSerialRpc",
    author="Gabriele Maris",
    author_email="gabriele.maris@mauxilium.it",
    license="Apache2",
    classifiers=[
        "License :: OSI Approved :: Apache Software License",
        "Programming Language :: Python :: 3.7",
    ],
    packages=["arduinopythonserialrpc", "arduinopythonserialrpc.engine", "arduinopythonserialrpc.exception"],
    include_package_data=True,
    install_requires=[
        "pyserial", "pytest"
    ]
)