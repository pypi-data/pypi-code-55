import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="jeffbarr", 
    version="0.1.1",
    author="edubz-mcgee",
    author_email="egwebber@amazon.com",
    description="For showing shiny pictures of the one, the only, Jeff Barr.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/EmilyWebber/jeff-barr",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)