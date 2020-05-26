import pathlib
from setuptools import find_packages, setup

HERE = pathlib.Path(__file__).parent

README = (HERE / "README.md").read_text()

setup(
    name="datascientist",
    version="0.1.6",
    description="A light set of enablers based on Cloudframe's proprietary data science codebase.",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/cloudframe/datascientist",
    author="Cloudframe Analytics",
    author_email="info@cloudframe.io",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
    ],
    packages=find_packages(),
    include_package_data=True,
    install_requires=["pandas", "numpy", "boto3", "psycopg2", "PyYAML"]
)
