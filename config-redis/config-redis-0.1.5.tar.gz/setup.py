import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="config-redis",
    version="0.1.5",
    author="RoyXing",
    author_email="x254724521@hotmail.com",
    description="Get proj config args from redis",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/x254724521/proj_config",
    packages=setuptools.find_packages(exclude=('tests',)),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
    install_requires=['redis==3.5.2']
)
