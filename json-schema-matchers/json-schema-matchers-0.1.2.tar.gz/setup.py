from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="json-schema-matchers",
    version="0.1.2",
    author="Jamal Zeinalov",
    author_email="jamal.zeynalov@gmail.com",
    description="PyHamcrest matchers extension for json schema validation",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/JamalZeynalov/json-schema-matchers",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=[
        'jsonschema==3.2.0',
        'PyHamcrest==2.0.2'
    ],
    python_requires='>=3.6',
)
