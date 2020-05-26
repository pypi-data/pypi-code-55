import setuptools

with open("readme.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="DalineUnitGenerator",
    version="0.0.9",
    author="kun.z",
    author_email="kun.z@daline.com.cn",
    description="test package",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/DalineWH",
    packages=['CodePackage'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    keywords='daline PU',
    install_requires=[
        'requests',
    ],
)