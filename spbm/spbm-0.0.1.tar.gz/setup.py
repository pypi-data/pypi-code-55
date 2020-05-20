import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="spbm",
    version="0.0.1",
    author="John Alcher Doloiras",
    author_email="johnalcherdoloiras@gmail.com",
    description="A set of handful benchmark utilities",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/alchermd/sbmp",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)