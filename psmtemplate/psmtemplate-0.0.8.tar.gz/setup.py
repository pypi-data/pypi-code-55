import setuptools

with open("README.md","r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="psmtemplate",
    version="0.0.8",
    author="Jianan Jiang",
    author_email="jianan.jiang@psm.com.au",
    description="PSM Templates",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=setuptools.find_packages(),
    install_requires=["reportlab","matplotlib","pdfrw","pillow","importlib_resources ; python_version<'3.7'"],
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
    zip_safe = False,
    include_package_data = True
)