from setuptools import setup


def README():
    with open("README.md") as file:
        return file.read()


def requirements():
    with open("requirements.txt") as file:
        return file.read().split("\n")


setup(
    name="uzautoprom",
    version="1.0",
    author="LidaRandom",
    author_email="bahoralievdev@yandex.com",
    description="Simple contracts loader with storage and filtering functionality for official UzAuto dealers.",
    long_description=README(),
    long_description_content_type="text/markdown",
    url="https://github.com/IlhomBahoraliev/uzautoprom",
    packages=["uzautoprom"],
    install_requires=requirements(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6"
)