# from distutils.core import setup
from setuptools import find_packages, setup

with open("README.rst", "r") as fh:
    long_description = fh.read()

setup(
    name="muscad",
    version="0.2.0",
    description="Generating OpenSCAD from Python code",
    long_description=long_description,
    long_description_content_type="text/x-rst",
    author="Guillaume Pujol",
    author_email="guill.p.linux@gmail.com",
    url="https://gitlab.com/guillp/muscad",
    classifiers=[
        "Programming Language :: Python",
        "Programming Language :: Python :: 3.6",
        "Development Status :: 4 - Beta",
        "Environment :: Other Environment",
        "Intended Audience :: Developers",
        "Intended Audience :: Manufacturing",
        "Intended Audience :: Science/Research",
        "Intended Audience :: Education",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Multimedia :: Graphics :: 3D Modeling",
    ],
    packages=find_packages(),
)
