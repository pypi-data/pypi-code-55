from setuptools import setup, find_packages

with open("README.md", "r") as f:
    long_description = f.read()

s = setup(
    name="zeebe_worker",
    version="0.2.0",
    license="MIT",
    description="An easy worker wrapper to create Zeebe Workers",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://gitlab.com/satys/libraries/zeebe-worker-py",
    packages=find_packages(),
    install_requires=[
        "grpcio>=1,<=2",
        "protobuf>=3,<=4",
        "zeebe-grpc==0.23.1.0"
    ],
    python_requires = ">= 3.5",
    author="Satys",
    author_email="info@satys.nl",
)
