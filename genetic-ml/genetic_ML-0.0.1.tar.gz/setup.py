import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="genetic_ML", 
    version="0.0.1",
    author="Eliot Kalfon",
    author_email="eliott.kalfon@gmail.com",
    description="in construction",
    long_description="in construction",
    long_description_content_type="text/markdown",
    url="https://github.com/eliottkalfon",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)