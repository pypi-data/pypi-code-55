import setuptools

setuptools.setup(
    name="pipedrive",
    version="0.2.0",
    author="Ondrej Sika",
    author_email="ondrej@ondrejsika.com",
    description="Pipedrive Client",
    url="https://github.com/ondrejsika/pipedrive",
    packages=setuptools.find_packages(),
    python_requires=">=3.6",
    install_requires=["requests"],
)
