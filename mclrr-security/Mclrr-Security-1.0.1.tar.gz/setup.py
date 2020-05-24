import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="Mclrr-Security",
    version="1.0.1",
    author="Maxence Raballand",
    author_email="maxenceraballand00@gmail.com",
    description="Package to encode and check passwords",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/maxencerb/Mclrr_Security",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)