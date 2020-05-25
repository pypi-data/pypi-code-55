import setuptools


with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="mlnames",
    version="0.0.1",
    author="Seungjae Ryan Lee",
    author_email="seungjaeryanlee@github.com",
    description="Name generator that uses machine learning vocabulary.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/seungjaeryanlee/mlnames",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)
