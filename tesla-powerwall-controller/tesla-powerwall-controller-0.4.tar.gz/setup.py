import setuptools

with open("README", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="tesla-powerwall-controller",
    version="0.4",
    author="samtherussell",
    description="Python controller for reading tesla powerwall status",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/samtherussell/tesla-powerwall-controller",
    packages=setuptools.find_packages(),
    install_requires=[
      "requests",
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
