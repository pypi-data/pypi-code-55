import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="gspoty",
    version="0.0.1",
    author="Diego Ramírez",
    author_email="diegocrzt@gmail.com",
    description="A spotify list extractor",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/diegocrzt/gspoty",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)