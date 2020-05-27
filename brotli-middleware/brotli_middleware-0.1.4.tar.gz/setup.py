"""A compression AGSI middleware using brotli.

Built using starlette under the hood, it can be used as a drop in replacement to
GZipMiddleware for Starlette or FastAPI.
"""

from setuptools import setup  # type: ignore

setup(
    name="brotli_middleware",
    version="0.1.4",
    url="",
    license="",
    author="Diogo B Freitas",
    author_email="somnium@riseup.net",
    description="A compression AGSI middleware using brotli",
    long_description=__doc__,
    packages=["brotli_middleware"],
    python_requires=">=3.5",
    include_package_data=True,
    install_requires=[
        "starlette>=0.13.4",
        "brotli @ git+https://github.com/google/brotli",
    ],
    # dependency_links=["git+https://github.com/google/brotli/tarball/master"],
    platforms="any",
    zip_safe=False,
    classifiers=[
        "Environment :: Web Environment",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
    ],
)
