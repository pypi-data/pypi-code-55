import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="slimz",
    version="0.0.5",
    author="scott",
    author_email="mbp98k@gmail.com",
    description="utils for python",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/scott-x/pyutils",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=[
            'xlrd',
            'xlwt',
            'xlutils',
            'colorama'
    ]
)