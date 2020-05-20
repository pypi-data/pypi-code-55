from setuptools import setup, find_packages

with open("README.md", "r") as readme_file:
    readme = readme_file.read()

requirements = ["pillow"]

setup(
    name="generatedateimage",
    version="0.0.4",
    author="Mahesh Bansod",
    author_email="mahesh0bansod@gmail.com",
    description="A package which creates an image which shows the current date",
    long_description=readme,
    long_description_content_type="text/markdown",
    url="https://github.com/maheshbansod/generatedateimage",
    packages=find_packages(),
    install_requires=requirements,
    license="MIT",
    classifiers=[
       "License :: OSI Approved :: MIT License",
       "Programming Language :: Python :: 3",
       "Programming Language :: Python :: 3.7",
    ],
)
