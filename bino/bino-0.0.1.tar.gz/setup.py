import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="bino", # Replace with your own username
    version="0.0.1",
    author="Arun I",
    author_email="isarun20@gmail.com",
    description="A small example package to convert decimal numbers to binary",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Arun1106/binary",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
