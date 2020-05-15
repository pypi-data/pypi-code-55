# -*- coding: utf-8 -*-
"""Installer for the collective.fhirpath package."""

from setuptools import find_packages
from setuptools import setup


long_description = "\n\n".join(
    [
        open("README.rst").read(),
        open("RESTAPI.rst").read(),
        open("CONTRIBUTORS.rst").read(),
        open("CHANGES.rst").read(),
    ]
)

install_requires = [
    "setuptools",
    # -*- Extra requirements: -*-
    "z3c.jbot",
    "plone.api>=1.10.1",
    "plone.restapi",
    "plone.app.dexterity",
    "collective.elasticsearch>=3.0.4",
    "plone.app.fhirfield>=3.1.0",
    "fhirpath>=0.6.1",
]

test_requires = [
    "plone.app.testing",
    # Plone KGS does not use this version, because it would break
    # Remove if your package shall be part of coredev.
    # plone_coredev tests as of 2016-04-01.
    "plone.testing>=7.0.1",
    "plone.app.contenttypes",
    "plone.app.robotframework[debug]",
    "collective.MockMailHost"
]

docs_requirements = [
    "sphinx",
    "sphinx-rtd-theme",
    "sphinxcontrib-httpdomain",
    "sphinxcontrib-httpexample",
]


setup(
    name="collective.fhirpath",
    version="0.4.0",
    description="Plone powered provider for fhirpath",
    long_description=long_description,
    # Get more from https://pypi.org/classifiers/
    classifiers=[
        "Environment :: Web Environment",
        "Development Status :: 4 - Beta",
        "Framework :: Plone",
        "Framework :: Plone :: Addon",
        "Framework :: Plone :: 5.2",
        "Framework :: Plone :: 5.3",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Operating System :: OS Independent",
        "License :: OSI Approved :: GNU General Public License v2 (GPLv2)",
    ],
    keywords="Python Plone FHIR Healthcare HL7",
    author="Md Nazrul Islam",
    author_email="email2nazru@gmail.com",
    url="https://github.com/collective/collective.fhirpath",
    project_urls={
        "PyPI": "https://pypi.python.org/pypi/collective.fhirpath",
        "Source": "https://github.com/collective/collective.fhirpath",
        "Tracker": "https://github.com/collective/collective.fhirpath/issues",
        'Documentation': 'https://collective-fhirpath.readthedocs.io/en/latest/',
    },
    license="GPL version 2",
    packages=find_packages("src", exclude=["ez_setup"]),
    namespace_packages=["collective"],
    package_dir={"": "src"},
    include_package_data=True,
    zip_safe=False,
    python_requires=">=3.7",
    install_requires=install_requires,
    extras_require={
        "test": test_requires + docs_requirements,
        "docs": docs_requirements,
    },
    entry_points="""
    [z3c.autoinclude.plugin]
    target = plone
    [console_scripts]
    update_locale = collective.fhirpath.locales.update:update_locale
    """,
)
