import setuptools
import os

with open("README.md", "r") as fh:
    long_description = fh.read()

buildnumber = os.environ.get('BUILDNUMBER') or 1

setuptools.setup(
    name="xtelligent-serial", # Replace with your own username
    version='0.0.{0}'.format(buildnumber),
    author="Xtelligent",
    author_email="development@xtelligent.io",
    description="Python object serialization focused on JSON",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/xtelligent/xtelligent-serial.git",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.7',
)
