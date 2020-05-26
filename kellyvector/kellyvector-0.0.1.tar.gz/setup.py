from setuptools import setup, find_packages

classifiers = [
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent"
        ]

setup(
        name = "kellyvector",
        version = "0.0.1",
        description = "Module for multi-dimentional vector calculations",
        long_description = open("README.txt").read(),
        url = "",
        author = "Giorgio Abbadessa",
        author_email = "gio.abbadessa@gmail.com",
        license = "MIT",
        classifiers = classifiers,
        keywords = "vector",
        packages = find_packages(),
        install_requires = [""]
        )


