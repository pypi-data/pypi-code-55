import os

from setuptools import setup, find_packages
from pathlib import Path

long_description: str = Path(Path.cwd(), "README.md").read_text()
version: str = os.environ.get("RELEASE_VERSION")

setup(
    name="AutoMD",
    version=version,
    url="https://github.com/cliftbar/automd",
    license="MIT",
    author="Cameron Barclift",
    author_email="cwbarclift@gmail.com",
    description="AutoMD is a documentation library for Flask APIs build with FlaskRESTful and Webargs.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=find_packages(include=["automd", "automd.*"]),
    python_requires=">=3.6",
    zip_safe=False,
    include_package_data=True,
    platforms="any",
    install_requires=[
        "flask",
        "flask-restful",
        "webargs",
        "apispec",
        "pyyaml",
        "marshmallow",
        "werkzeug"
    ],
    classifiers=[
        "Environment :: Web Environment",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Topic :: Internet :: WWW/HTTP :: Dynamic Content",
        "Topic :: Software Development :: Libraries :: Python Modules"
    ]
)
