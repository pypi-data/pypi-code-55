import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="abcdefgh", # Distribution name
    version="0.0.1",
    author="Alexia Montalant",
    author_email="alexia.montalant@orange.fr",
    description="A package for electrophysiology data analysis",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="", # Link to github
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)