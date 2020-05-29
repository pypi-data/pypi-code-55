import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="logfast",
    version="0.3.3",
    author="Adrian Thoenig",
    description="Quick and easy logging initialization",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/ThoenigAdrian/logfast",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=2.5',
    setup_requires=['wheel'],
)
