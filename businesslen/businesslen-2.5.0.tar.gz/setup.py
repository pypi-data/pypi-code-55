import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="businesslen",
    version="2.5.0",
    author="Cuong Dang",
    author_email="cuongd@pm.me",
    description="Calculate business days/hours between two datetimes",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/cuong-dang/businesslen",
    packages=setuptools.find_packages(),
    install_requires=["holidays"],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ]
)
