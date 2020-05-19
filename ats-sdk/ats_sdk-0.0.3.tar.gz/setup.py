import setuptools

setuptools.setup(
    name="ats_sdk",
    version="0.0.3",
    description="SDK for alternate text service",
    url="https://github.com/shuttl-tech/ats_sdk",
    author="Shuttl",
    author_email="pratik.singh@shuttl.com",
    license="MIT",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3.7",
        "License :: OSI Approved :: MIT License",
    ],
    install_requires=["requests", "pyshuttlis", "cachetools"],
    extras_require={
        "test": [
            "pytest",
            "pytest-runner",
            "pytest-cov",
            "pytest-pep8",
            "responses",
            "bumpversion",
        ]
    },
)
