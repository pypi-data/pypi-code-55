import setuptools
 
with open("README.md", "r") as fh:
    long_description = fh.read()
 
setuptools.setup(
    name="Arsla",
    version="0.0.1",
    author="Nitin Gupta",
    author_email="nitingpt000@gmail.com",
    description="Basic calculation using numbers",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://datosbit.com/",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)