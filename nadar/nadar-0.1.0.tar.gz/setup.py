import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="nadar", # Replace with your own username
    version="0.1.0",
    author="Michal Puchala",
    author_email="mk.puchala@gmail.com",
    description="NAtural DAte Ranges - automatic translation of natural language phrases describing date ranges into relevant dates or strings",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/michalpuchala/nadar",
    packages=['nadar'],
    install_requires=[
        'datetime',
        'dateparser'
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)