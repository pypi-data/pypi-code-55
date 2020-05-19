from setuptools import setup, find_namespace_packages

setup(
    name="scidra-module-utils",
    description="Utilities and Classes to create scidra compatible modules",
    version="0.2.0",
    packages=find_namespace_packages(include=["scidra.*"]),
    install_requires=["click", "humps", "pydantic", "requests", "clint", "loguru"],
)
