import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="gcheat",
    version="0.0.1",
    author="Karl Berggren",
    author_email="kalle@jjabba.com",
    description="A on point lib for reading and writing to google sheets.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/jjabba/gcheat",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
