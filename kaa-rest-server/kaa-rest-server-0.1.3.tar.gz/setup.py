import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="kaa-rest-server",
    version="0.1.3",
    author="Francesc d'Assís Requesens i Roca",
    author_email="francesc.requesens@gmail.com",
    description="A very simple REST server",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/elpeix/kaa",
    packages=setuptools.find_packages(
        exclude=[
            "*.tests", "*.tests.*", "tests.*", "tests",
            "example.*","example"
        ]),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    install_requires=['pyyaml']
)
