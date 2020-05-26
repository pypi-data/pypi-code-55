import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="pyplayground-ralfeus", # Replace with your own username
    version="0.0.1",
    author="Mychajlo Chodorev",
    author_email="ralfeus@gmail.com",
    description="Module to create simple games using pygame",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/ralfeus/pyplayground",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    install_requires=[
        'numpy',
        'pygame'
    ]
)