import setuptools

with open("README.md", "r") as fh:
    long_description = ""

setuptools.setup(
    name="indicis", 
    version="0.0.2",
    author="Gustavo Barros",
    author_email="gustavo.barros@jurus.com.br",
    description="Bibliotera de parser para indices do mercado brasileiro",
    long_description="Bibliotera de parser para indices do mercado brasileiro como DI, DI Futuro e IPCA.",
    long_description_content_type="text/markdown",
    url="https://github.com/jurusbr/indicis",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)