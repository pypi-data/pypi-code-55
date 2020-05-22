import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="scprint",
    version="1.0.1b0",
    author="Daniel Gill",
    author_email="DanG_@outlook.com",
    description="None",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/DanGill/scprint",
    py_modules=["scprint", "colorsToHex"],
    packages=setuptools.find_packages(),
    keywords="None",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
    ],
    python_requires='~=3.3',
)