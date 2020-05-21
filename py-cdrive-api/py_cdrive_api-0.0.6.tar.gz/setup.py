import setuptools                                                                        

with open("README.md", "r") as fh: 
    long_description = fh.read() 

setuptools.setup(
    name="py_cdrive_api",
    version="0.0.6",
    author="ColumbusTech",
    author_email="columbustechio@gmail.com",
    description="Python API for CDrive",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/columbustech/py-cdrive-api",
    packages=setuptools.find_packages(),
    install_requires=[
        "requests",
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: BSD License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
