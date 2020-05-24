import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="myasicAPI", # Replace with your own username
    version="0.2.5",
    author="@MyAsic",
    author_email="baikal-interspace@eyandex.com",
    description="API for MyAsic project",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/MiningManufacture/MyAsic.git",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
