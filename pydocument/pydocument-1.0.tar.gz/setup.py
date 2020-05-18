from setuptools import setup

long_description = open("README.md", "r").read()

setup(
    name="pydocument",
    packages=["pydocument"],
    version="1.0",
    license="UNLICENSED",
    description="Easy way to make documents with gui (tkinter)",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Jack Murrow",
    author_email="jack.murrow122005@gmail.com",
    keywords=["PyDocument", "Python Document", "Document"],
    classifiers=[
        "Programming Language :: Python :: 3"
    ]
)