import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="genie_aladdin",
    version="2020.05.01",
    author="Aijay Adams",
    author_email="aijay.adams@gmail.com",
    description="Client for connecting to the Genie Aladdin connected garage door opener",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/pypa/genie_aladdin",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.7',
)
