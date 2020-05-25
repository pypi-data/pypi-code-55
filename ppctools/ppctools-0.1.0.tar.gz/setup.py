import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="ppctools",
    version="0.1.0",
    author="Roman Trapeznikov",
    author_email="roma190505@yandex.ru",
    description="PPC tools for CTF tasks",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Dliwk/ppctools",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: Freeware",
    ],
    python_requires='>=3.6',
)