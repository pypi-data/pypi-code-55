import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="imagepreprocessing",
    version="1.5.0",
    author="Can Kurt",
    author_email="can.kurt.aa@gmail.com",
    description="image preprocessing",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/cccaaannn/imagepreprocessing",
    packages=setuptools.find_packages(exclude=['test.py', ]),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)   