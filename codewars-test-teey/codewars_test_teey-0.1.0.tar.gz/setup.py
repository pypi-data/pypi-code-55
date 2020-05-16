from setuptools import setup

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="codewars_test_teey",
    version="0.1.0",
    author="Codewars",
    packages=["codewars_test"],
    license="MIT",
    description="Codewars test framework for Python (fork)",
    long_description=long_description,
    long_description_content_type="text/markdown",
    install_requires=[],
    url="https://github.com/teey-t/python-test-framework",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
