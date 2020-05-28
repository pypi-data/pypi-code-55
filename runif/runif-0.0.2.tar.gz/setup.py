import io
import re
from setuptools import setup

with io.open("README.rst", "rt", encoding="utf8") as f:
    readme = f.read()

with io.open("runif/__init__.py", "rt", encoding="utf8") as f:
    version = re.search(r"__version__ = '(.*?)'", f.read()).group(1)

setup(
    name="runif",
    version=version,
    url="https://gioorgi.com/2020/runif/",
    project_urls={
        "Documentation": "https://github.com/daitangio/runif",
        "Code": "https://github.com/daitangio/runif",
        "Issue tracker": "https://github.com/daitangio/runif/issues",
    },
    license="BSD-3-Clause",
    author="Giovanni Giorgi",
    author_email="jj@gioorgi.com",
    maintainer="Giovanni Giorgi",
    maintainer_email="jj@gioorgi.com",
    description="Idempotent and minimal python library for rapid scripting.",
    long_description=readme,
    packages=["runif"],
    include_package_data=True,
    python_requires=">=3.6",
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: BSD License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
    ],
)