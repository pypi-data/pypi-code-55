import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="numpyprint",  # Replace with your own username
    version="0.1.4",
    author="Daniel Steinegger",
    author_email="steinegger.daniel@gmail.com",
    description="prints numpy arrays nicely",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://gitlab.com/steinegger.daniel/numpyprint",
    packages=setuptools.find_packages(),
    py_modules=["numpyprint"],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
