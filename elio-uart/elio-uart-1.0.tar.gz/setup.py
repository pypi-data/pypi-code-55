#-*- coding:utf-8 -*-

import setuptools

setuptools.setup(
    name="elio-uart",
    version="1.0",
    license='MIT',
    author="elio robotics",
    author_email="caram88@mobilian.biz",
    description="elio board python interface",
    long_description=open('README.md').read(),
    url="https://github.com/johnsnow-nam",
    packages=setuptools.find_packages(),
    classifiers=[
        # 패키지에 대한 태그
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent"
    ],
)