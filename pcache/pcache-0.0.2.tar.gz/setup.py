from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="pcache",
    version="0.0.2",
    author="Pallab Pain",
    author_email="pallabkumarpain@gmail.com",
    description="A simple implementation of Persistent Caching",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/pallabpain/pcache.git",
    license="MIT",
    packages=["pcache"],
    keywords=["cache", "persistent cache"],
    classifiers=[
        "Development Status :: 3 - Alpha",
        "License :: OSI Approved :: MIT License",
        "Operating System :: Unix",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
    ],
)
