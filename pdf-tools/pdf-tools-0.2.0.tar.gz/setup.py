import os
from io import open
from setuptools import setup
from setuptools import find_packages

here = os.path.abspath(os.path.dirname(__file__))

with open(os.path.join(here, "README.md"), "r", encoding="utf-8") as fobj:
    long_description = fobj.read()

with open(os.path.join(here, "requirements.txt"), "r", encoding="utf-8") as fobj:
    requires = fobj.readlines()
requires = [x.strip() for x in requires]

setup(
    name="pdf-tools",
    version="0.2.0",
    description="PDF tools, e.g. pdf2images, images2pdf, pdf2text, pdf2html, pdfmeta...",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="zencore-cn",
    author_email="info@zencore.cn",
    license="MIT",
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3 :: Only",
    ],
    keywords=["pdf-tools", "images2pdf", "pdf2images", "pdf2html", "pdf2text", "pdfmeta"],
    requires=requires,
    install_requires=requires,
    packages=find_packages("."),
    py_modules=["pdf_tools"],
    entry_points={
        "console_scripts": [
            "images2pdf = pdf_tools:images2pdf",
            "pdf2images = pdf_tools:pdf2images",
            "pdf2html = pdf_tools:pdf2html",
            "pdf2text = pdf_tools:pdf2text",
            "pdfmeta = pdf_tools:pdfmeta",
        ]
    },
)
