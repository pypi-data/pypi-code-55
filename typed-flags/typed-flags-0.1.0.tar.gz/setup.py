from setuptools import find_packages, setup

with open("README.md") as f:
    long_description = f.read()

setup(
    name="typed-flags",
    version="0.1.0",
    author="Thomas Kehrenberg",
    author_email="t.kehrenberg@sussex.ac.uk",
    description="Typed Flags",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/thomkeh/typed-flags",
    license="Apache",
    packages=find_packages(),
    package_data={"typed_flags": ["py.typed"]},
    install_requires=[],
    classifiers=[
        "Programming Language :: Python :: 3.8",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
        "Typing :: Typed",
    ],
    keywords=["typing", "argument parser", "python"],
)
