from setuptools import find_packages
from setuptools import setup


def readme():
    with open("README.md") as readme:
        return readme.read()


setup(
    name="pyiocontrol",
    version="0.7.4",
    description="iocontrol.ru module for iocontorl.ru api",
    long_description=readme(),
    long_description_content_type="text/markdown",
    classifiers=["Programming Language :: Python :: 3"],
    url="http://github.com/tremaru/pyiocontrol",
    author="iocontrol.ru",
    author_email="info@iocontrol.ru",
    include_package_data=True,
    packages=find_packages(exclude=("tests",)),
    license="MIT",
    install_requires=["requests==2.23.0"],
)
