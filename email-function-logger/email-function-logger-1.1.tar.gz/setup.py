import setuptools
from pip._internal.req import parse_requirements

with open("README.md", "r") as fh:
    long_description = fh.read()


requires = ['requests==2.23.0']


setuptools.setup(
    name="email-function-logger",
    version="1.1",
    author="Arthur Cerveira",
    author_email="aacerveira@inf.ufpel.edu.br",
    description="A decorator to log information about a function and send it to your email",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/arthurcerveira/Email-Function-Logger",
    download_url="https://github.com/arthurcerveira/Email-Function-Logger/archive/v1.1.tar.gz",
    packages=setuptools.find_packages(),
    keywords=['log', 'email', 'function', 'logger'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=requires,
    python_requires='>=3.2',
)
