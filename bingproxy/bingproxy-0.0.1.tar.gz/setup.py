import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="bingproxy", # Replace with your own username
    version="0.0.1",
    author="Thomas Tong",
    author_email="k.thomas.tong@gmail.com",
    description="An implementation of daynamic proxy",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/sherocktong/bingproxy",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.5',
) 
