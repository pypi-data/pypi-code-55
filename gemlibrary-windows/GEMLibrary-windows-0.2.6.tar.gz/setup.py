import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="GEMLibrary-windows",
    version="0.2.6",
    include_package_data=True,
    author="Kevin Morgan",
    author_email="KMorgan@teleioscommodities.com",
    description="GEM Derivatives Library",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: Other/Proprietary License",
        "Operating System :: Microsoft :: Windows :: Windows 10",
    ],
    python_requires='>=3.6',
)
