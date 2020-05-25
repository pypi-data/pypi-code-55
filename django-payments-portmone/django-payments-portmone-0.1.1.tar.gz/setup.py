from setuptools import find_packages, setup

version = "0.1.1"

requirements = ["Django>=1.11", "django-payments>=0.12"]

extras_require = {
    "test": ["pytest-cov", "pytest-django", "pytest"],
    "lint": ["flake8", "wemake-python-styleguide", "isort"],
}

extras_require["dev"] = extras_require["test"] + extras_require["lint"]  # noqa: W504

with open("README.md", "r", encoding="utf-8") as readme:
    long_description = readme.read()


setup(
    name="django-payments-portmone",
    author="Vyacheslav Onufrienko",
    author_email="onufrienkovi@gmail.com",
    description="A django-payments backend for the Portmone payment gateway",
    long_description=long_description,
    long_description_content_type="text/markdown",
    version=version,
    url="https://github.com/onufrienkovi/django-payments-portmone",
    extras_require=extras_require,
    packages=find_packages(exclude=["tests", "scripts"]),
    install_requires=requirements,
    python_requires=">=3.6",
    classifiers=[
        "Environment :: Web Environment",
        "Framework :: Django",
        "Intended Audience :: Developers",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Topic :: Internet :: WWW/HTTP",
        "Topic :: Software Development :: Libraries :: Application Frameworks",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
)
