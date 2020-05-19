# -*-coding:utf-8-*-
__author__ = 'Dragon Sun'

import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="dsQtCommon",
    keywords="dsQtCommon",
    version="0.0.4",
    author="Dragon Sun",
    author_email="dragonsun7@163.com",
    license="MIT",
    description="DS's Quantized Transaction common library.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://gitee.com/dragonsun7/dsQtCommon.git",
    packages=setuptools.find_packages(),
    include_package_data=True,
    zip_safe=True,
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=[
        "dsPyLib",
    ],
    python_requires='>=3.6',
)
