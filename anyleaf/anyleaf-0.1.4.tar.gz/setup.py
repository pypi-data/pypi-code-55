import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="anyleaf",
    version="0.1.4",
    author="Anyleaf",
    author_email="david.alan.oconnor@gmail.com",
    description="Driver for the Anyleaf pH sensor",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/anyleaf/anyleaf_ph",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
        "Topic :: System :: Hardware :: Hardware Drivers ",
    ],
    python_requires=">=3.7",
    license="MIT"
)
