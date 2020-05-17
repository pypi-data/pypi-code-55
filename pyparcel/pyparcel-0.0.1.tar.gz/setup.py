import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="pyparcel",
    version="0.0.1",
    author="Nathan Cohen",
    author_email="ncohen4299@gmail.com",
    description="Easy to use binary packer that doesn't require struct's specifications",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/najaco/PyParcel",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
