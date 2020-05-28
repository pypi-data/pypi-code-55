"""timecast: an library for online time series analysis"""
import datetime
import os
import sys

from setuptools import find_packages
from setuptools import setup

name = "timecast"
version = "0.2.7"

if "--nightly" in sys.argv:
    name += "-nightly"

    date_suffix = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
    version += ".dev" + date_suffix
    sys.argv.remove("--nightly")
    print(name, version)

with open(
    os.path.join(os.path.abspath(os.path.dirname(__file__)), "README.md"), encoding="utf-8",
) as f:
    long_description = f.read()

setup(
    name=name,
    version=version,
    author="Google AI Princeton",
    author_email="dsuo@google.com",
    description="Performant, composable online learning",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/MinRegret/timecast",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    keywords=["timeseries", "time", "series", "analysis", "online", "learning"],
    python_requires=">=3.6",
    install_requires=["numpy", "jax", "jaxlib", "flax", "pandas", "pathos", "tqdm"],
    extras_require={
        "dev": [
            "flake8",
            "flake8-print",
            "flake8-bugbear",
            "mypy",
            "scikit-learn",
            "pytest",
            "pytest-cov",
            "pytest-instafail",
            "pytest-xdist",
            "pylint",
            "black",
            "reorder-python-imports",
            "autoflake",
            "pre-commit",
            "pydocstring-coverage",
            "bumpversion",
            "ipython",
            "jupyter",
            "gprof2dot",
            "bandit",
            "check-python-versions",
            "line-profiler",
        ],
        "docs": ["sphinx", "sphinxcontrib-napoleon", "sphinx_rtd_theme"],
    },
)
