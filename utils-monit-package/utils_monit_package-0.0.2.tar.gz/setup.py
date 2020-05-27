import setuptools

fh=open("README.md","r")

long_description=fh.read()

fh.close()

#author author_email --> account PyPI
setuptools.setup(
    name="utils_monit_package",
    version="0.0.2",
    author="Antonio",
    author_email="fabanto.dev@gmail.com",
    description="",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="",
    setup_requires=['wheel'],
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)