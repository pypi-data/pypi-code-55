# from distutils.core import setup

import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="dld_array_generator", # Replace with your own username
    version="1.0.4",
    author="Morten Kals",
    author_email="dev@mkals.no",
    description="Python package to generate parameterized DLD arrays.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/mkals/dld_array_generator",
    packages=setuptools.find_packages(),
    install_requires=['numpy', 'ezdxf'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
