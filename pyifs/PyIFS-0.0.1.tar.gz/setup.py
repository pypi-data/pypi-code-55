import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="PyIFS",
    version="0.0.1",
    author="nightwnvol",
    author_email="notte_94@hotmail.it",
    description="A python3 package for infinite feature selection",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://https://github.com/InfOmics/PyIFS",
    packages=setuptools.find_packages(),
    install_requires=[
        "numpy"
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)