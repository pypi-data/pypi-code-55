from setuptools import setup

def readme():
    with open('README.md') as f:
        README = f.read()
    return README

setup(
    name="greetings-Shiloh6",
    version="1.1.0",
    description="A Python package that can say greetings in python.",
    long_description=readme(),
    long_description_content_type="text/markdown",
    url="https://github.com/Shiloh6/Greetings",
    author="Shiloh Hiebert",
    author_email="shilohhiebert@gmail.com",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
    ],
    packages=["greetings"],
    include_package_data=True,
)