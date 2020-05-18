from setuptools import find_namespace_packages, setup

with open("src/README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="robomotion", # Replace with your own username
    version="1.0.3",
    author="Robomotion IO",
    author_email="support@robomotion.io",
    description="Robomotion custom node package",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/pypa/sampleproject",
    include_package_data=True,
    packages=["."],
    package_dir={"": "src"},
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)