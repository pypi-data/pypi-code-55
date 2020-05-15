import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="getConfig", # Replace with your own username
    version="0.0.1",
    author="Alex-Martin Lakovski",
    author_email="amkl17mz@gmail.com",
    description="Python module for reading variables from configuration files like cfg, INI, XML, JSON.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/AlexMartin17/getConfig",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
