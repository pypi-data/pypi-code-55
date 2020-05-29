import os
from distutils.core import setup
from setuptools import find_packages


def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()


setup(
    name="pysin",
    packages=find_packages(),
    version="1.0.1",
    license="Apache License 2.0",
    description="PySin is a toolbox for text retrieval in unstructured documents datasets. It contains both a multi-type text extractor and a search engine. To test them, you can use the medical prescriptions generator that is also provided.",
    author="Jean-Baptiste Laval",
    author_email="contact@arkhn.com",
    url="https://github.com/arkhn/PySin",
    download_url="https://github.com/arkhn/PySin/archive/1.0.1.tar.gz",
    keywords=[
        "arkhn",
        "text retrieval",
        "search engine",
        "text extraction",
        "dataset generator",
        "medical",
    ],
    install_requires=[
        'pandas==1.0.3',
        'fpdf==1.7.2',
        'Faker==4.1.0',
        'Unidecode==1.1.1',
        'docx2txt==0.8',
        'path.py==12.4.0',
        'pdftotext==2.1.4',
        'striprtf==0.0.10',
    ],
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Build Tools",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
    ],
)
