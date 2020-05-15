import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="spivolt",
    version="0.0.1",
    author="Nick Farnham",
    author_email="nick.farnham@southwales.ac.uk",
    description="A wrapper for the SPiVolt API.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/brythonick/spivolt",
    packages=setuptools.find_packages(include=["spivolt", "spivolt.*"], exclude=["tests", ]),
    install_requires=[
        "pandas",
        "requests",
        "numpy",
        "matplotlib"
    ],
    classifiers=[
        "Programming Language :: Python :: 3.6",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",
        "Development Status :: 2 - Pre-Alpha",
        "Topic :: Scientific/Engineering",
    ],
    python_requires='>=3.6',
)
