from structlog_ext_utils import __version__

from collections import OrderedDict

import setuptools


with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="structlog_ext_utils",
    version=f"{__version__}",
    author="alexandre menezes",
    author_email="alexandre.fmenezes@gmail.com",
    description="structlog extension utilities",
    long_description=long_description,
    long_description_content_type="text/markdown",
    license="Apache-2.0",
    url="https://github.com/amenezes/structlog_ext_utils",
    packages=setuptools.find_packages(include=["structlog_ext_utils", "structlog_ext_utils.*"]),
    python_requires=">=3.6.0",
    project_urls=OrderedDict(
        (
            ("Documentation", "https://structlog_ext_utils.amenezes.net"),
            ("Code", "https://github.com/amenezes/structlog_ext_utils"),
            ("Issue tracker", "https://github.com/amenezes/structlog_ext_utils/issues"),
        )
    ),
    install_requires=["structlog", "python-json-logger"],
    tests_require=[
        "pytest==5.3.4",
        "flake8==3.7.8",
        "pytest-cov==2.8.1",
        "isort==4.3.21",
        "black==19.10b0",
        "mypy>=0.761",
    ],
    extras_require={
        "docs": ["portray>=1.3.1"],
        "all": ["structlog", "python-json-logger", "portray>=1.3.1"],
    },
    setup_requires=["setuptools>=38.6.0"],
    classifiers=[
        "Intended Audience :: Developers",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: Implementation :: CPython",
        "Programming Language :: Python :: Implementation :: PyPy",
        "Topic :: Software Development :: Libraries",
    ],
)
