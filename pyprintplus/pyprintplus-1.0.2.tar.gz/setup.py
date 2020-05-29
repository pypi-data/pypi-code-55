import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="pyprintplus",
    version="1.0.2",
    author="Marco",
    author_email=None,
    description="A better way of printing logs in Python.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/marcoEDU/PyPrintPlus",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    install_requires=[]
)
