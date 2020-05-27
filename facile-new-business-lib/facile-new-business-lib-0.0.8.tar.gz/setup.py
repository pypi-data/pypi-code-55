import setuptools

with open("README.md", "r") as f:
    LONG_DESCRIPTION = f.read()

setuptools.setup(
    name="facile-new-business-lib",
    version="0.0.8",
    author="Fabio Lima",
    author_email="f46io@icloud.com",
    description="testing ",
    long_description_content_type="text/markdown",
    long_description=LONG_DESCRIPTION,
    url="https://www.facile.it",
    packages=["facilenewbusinesslib"],
    install_requires = [
            "selenium ~= 3.141.0",
            "robotframework ~= 3.2",
    ],
    Classfiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "License :: MIT",
        "Operating System  ::  OS Independent",
        "Facile.it New Business help out lib "
    ],
)
