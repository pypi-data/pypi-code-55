import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="CsPy_Uploading", # Replace with your own username
    version="0.1.8",
    author="James Robinson",
    author_email="james.robinson@thehutgroup.com",
    description="Package useful for THG staff to aid data pipeline implementation",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/JamesRobinson-THG/CsPy_Uploading/archive/0.1.8.tar.gz",
    packages=setuptools.find_packages(),
    classifiers=[
		"Development Status :: 3 - Alpha",
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)