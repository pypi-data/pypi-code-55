import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="autocp2k",
    version="0.0.1",
    author="Brian C. Ferrari",
    author_email="Brian.Ferrari@ucf.edu",
    description="This is a python module for automating CP2K calculations.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Cavenfish/autocp2k",
    packages=setuptools.find_packages(),
    install_requires=["numpy", "scipy", "pandas", "basis_set_exchange", "PeriodicElements",
                      "openpyxl", "matplotlib", "xlrd", "xlsxwriter"],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: Microsoft :: Windows :: Windows 10",
    ],
)
