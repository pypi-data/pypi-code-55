import pathlib
from setuptools import find_packages, setup

HERE = pathlib.Path(__file__).parent

README = (HERE / "README.md").read_text()

setup(
    name="startaker",
    version="0.0.9",
    description="The Cloudframe Data Science Environment",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/cloudframe/startaker",
    author="Cloudframe Analytics",
    author_email="info@cloudframe.io",
    license="",
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
    ],
    packages=find_packages(),
    include_package_data=True,
    install_requires=["datascientist", "boto3", "PyYAML"]
)
