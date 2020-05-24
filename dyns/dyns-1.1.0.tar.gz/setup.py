from setuptools import setup, find_packages

setup(
    name="dyns",
    version="1.1.0",
    description="Command line tool to interact with dyns API",
    url="https://github.com/xhs/dyns/dynsctl",
    author="Xiaohan Song",
    author_email="chef@dark.kitchen",
    classifiers=[
        "Development Status :: 4 - Beta",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
    ],
    packages=find_packages(exclude=["contrib", "docs", "tests"]),
    python_requires=">=3.6",
    install_requires=[
        "click>=7.1.2",
        "requests>=2.23.0",
        "rich>=1.2.2",
    ],
    scripts=['dynsctl']
)
