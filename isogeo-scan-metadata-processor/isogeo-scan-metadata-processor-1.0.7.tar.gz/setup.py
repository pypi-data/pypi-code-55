#! python3  # noqa: E265


"""
    Setup script to package into a Python module
"""

# ############################################################################
# ########## Libraries #############
# ##################################

# standard library
import pathlib

# 3rd party
from setuptools import find_packages, setup

# package (to get version)
from scan_metadata_processor import __about__

# ############################################################################
# ########### Globals ##############
# ##################################

# The directory containing this file
HERE = pathlib.Path(__file__).parent

# The text of the README file
README = (HERE / "README.md").read_text()

# ############################################################################
# ########## Packaging #############
# ##################################
setup(
    # metadata
    name="isogeo-scan-metadata-processor",
    version=__about__.__version__,
    author=__about__.__author__,
    author_email=__about__.__email__,
    description=__about__.__summary__,
    long_description=README,
    long_description_content_type="text/markdown",
    keywords="Isogeo scan JSON middleware",
    url=__about__.__uri__,
    project_urls={
        "Docs": "http://help.isogeo.com/scan/isogeo-scan-metadata-processor/",
        "Bug Reports": "{}issues/".format(__about__.__uri__),
        "Source": __about__.__uri__,
    },
    # implementation
    python_requires=">=3.6, <4",
    classifiers=[
        "Intended Audience :: Developers",
        "Intended Audience :: Information Technology",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Development Status :: 5 - Production/Stable",
        "Operating System :: OS Independent",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    # packaging
    py_modules=["scan_metadata_processor"],
    packages=find_packages(
        exclude=["contrib", "docs", "*.tests", "*.tests.*", "tests.*", "tests"]
    ),
    include_package_data=True,
    install_requires=[
        "click==7.1.*",
        "geojson>=2.5,<2.6",
        "isogeo-pysdk>=3.4,<3.5",
        "python-dotenv>=0.12,<0.14",
        "semver>=2.9,<2.11",
        "Send2Trash==1.5.*",
    ],
    extras_require={
        "dev": ["black", "flake8"],
        "db-elastic": ["elasticsearch>=7.5,<7.7"],
        "test": ["pytest", "pytest-cov"],
    },
    entry_points="""
        [console_scripts]
        scan-metadata-processor=scan_metadata_processor.cli:scan_metadata_processor
    """,
)
