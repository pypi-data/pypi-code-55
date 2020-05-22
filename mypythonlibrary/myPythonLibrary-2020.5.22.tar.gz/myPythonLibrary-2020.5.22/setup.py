import setuptools

setuptools.setup(
    name="myPythonLibrary",
    version="2020.05.22",
    author="Martin Genet",
    author_email="martin.genet@polytechnique.edu",
    description="A collection of python tools",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",
    ],
    # python_requires='>=3.6',
)
