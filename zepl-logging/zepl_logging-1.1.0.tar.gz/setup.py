import pathlib
from setuptools import setup

# The directory containing this file
HERE = pathlib.Path(__file__).parent

# The text of the README file
README = (HERE / "README.md").read_text()

# This call to setup() does all the work
setup(
    name="zepl_logging",
    version="1.1.0",
    description="Alternate Logging package for zepl",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/usama2762/zepl_logging_client",
    author="Usama Jamil",
    author_email="usamajamil77@gmail.com",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
    ],
    packages=["zepl_logging"],
    include_package_data=True,
    install_requires=["requests", "datetime"],
)