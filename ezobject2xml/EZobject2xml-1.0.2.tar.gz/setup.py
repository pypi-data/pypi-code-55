import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="EZobject2xml",
    version="1.0.2",
    author="Alexandre CHAPELLE",
    author_email="alexandre.chapelle@yahoo.fr",
    description="Easily save and load any object data to/from a xml file",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/JoshuaWar/EZobject2xml",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.8',
)
