import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="fenixapi",
    version="0.0.3",
    author="Francisco Rodrigues",
    author_email="francisco.rodrigues0908@gmail.com",
    description="An API to interface with fenix.tecnico.ulisboa.pt",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/ArmindoFlores/fenixapi",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
