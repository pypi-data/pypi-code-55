import setuptools


with open("README.md", "r") as fh:
    long_description = fh.read()


packages = setuptools.find_packages()



setuptools.setup(
    name="mrsdb2",
    version="2.2.2",
    author="Netriza",
    author_email="info@mrsdb.netriza.ml",
    description="The quick, rich, serverless, and efficient json-like Python 3 document database.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/netriza/mrsdb",
    packages=setuptools.find_packages(),
    install_requires=[
        'bson',
        'bcrypt'
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Topic :: Database",
        "Topic :: Database :: Database Engines/Servers"
    ],
    python_requires='>=3.6',
)
