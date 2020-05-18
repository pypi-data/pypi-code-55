import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="mrsdb2",
    version="2.1.0",
    author="Netriza",
    author_email="info@mrsdb.netriza.ml",
    description="The quick, rich, serverless, and efficient json-like Python 3 document database.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://netriza.github.io/mrsdb/",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)