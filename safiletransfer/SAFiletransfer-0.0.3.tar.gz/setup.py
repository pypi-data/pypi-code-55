import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="SAFiletransfer", 
    version="0.0.3",
    author="SurgeAnalytics",
    author_email="gleb@surgeanalytics.ca",
    description="none",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/pypa/surgeanalytics",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)