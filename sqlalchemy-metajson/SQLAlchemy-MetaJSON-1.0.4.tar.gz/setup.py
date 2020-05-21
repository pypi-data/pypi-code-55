import io

from setuptools import find_packages
from setuptools import setup

with io.open("README.rst", "rt", encoding="utf8") as f:
    readme = f.read()

setup(
    name="SQLAlchemy-MetaJSON",
    version="1.0.4",
    url="https://moesol.com/",
    license="BSD",
    maintainer="Moebius Solutions, Inc.",
    maintainer_email="support@moesol.com",
    description="Extract meta information on SQLAlchemy models to JSON.",
    long_description=readme,
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: BSD License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
    ],
    packages=find_packages("src"),
    package_dir={"": "src"},
    include_package_data=True,
    python_requires=">=3.6",
    install_requires=[],
    extras_require={
        "dev": [
            "Sphinx",
            "Pallets-Sphinx-Themes",
            "tox",
            "pytest",
            "coverage",
            "pytest-cov",
        ]
    },
)
