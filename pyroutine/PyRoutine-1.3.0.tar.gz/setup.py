import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="PyRoutine", 
    version="1.3.0",
    author="Atharv2",
    author_email="atharv260107@gmail.com",
    description="A program to redo mouse functions.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Atharv2/PyRoutine",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.0',
)
