import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

    tests_require = [
        "pytest>=3.6.3",
        "pytest-django>=3.3.2",
    ]


dev_requires = ["black==19.10b0",] + tests_require

setuptools.setup(
    name="graphene-t2",
    version="0.3.0",
    author="Röstäm Gazizov",
    author_email="gazizov@tn.ru",
    license="MIT",
    description="An extension for graphene",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/rustemg/graphene-t2",
    packages=setuptools.find_packages(exclude=["tests*"]),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Libraries",
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
    keywords="api graphql graphene",
    install_requires=["graphene>=2.1.7,<3", "graphene-django>=2.8,<3",],
    setup_requires=["pytest-runner"],
    tests_require=tests_require,
    extras_require={"test": tests_require, "dev": dev_requires,},
)
