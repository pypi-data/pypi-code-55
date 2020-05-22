import setuptools

setuptools.setup(
    name="myPythonLibrary",
    version="2020.05.22.post0",
    author="Martin Genet",
    author_email="martin.genet@polytechnique.edu",
    description="A collection of python tools",
    long_description = open("README.md", "r").read(),
    long_description_content_type="text/markdown",
    url="https://gitlab.inria.fr/mgenet/myPythonLibrary",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",
    ],
    install_requires=['numpy'],
    # python_requires='>=3.6',
)
