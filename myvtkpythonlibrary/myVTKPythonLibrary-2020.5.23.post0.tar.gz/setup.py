import setuptools

setuptools.setup(
    name="myVTKPythonLibrary",
    version="2020.05.23.post0",
    author="Martin Genet",
    author_email="martin.genet@polytechnique.edu",
    description=open("README.md", "r").readlines()[1][:-1],
    long_description = open("README.md", "r").read(),
    long_description_content_type="text/markdown",
    url="https://gitlab.inria.fr/mgenet/myVTKPythonLibrary",
    packages=["myVTKPythonLibrary"],
    license="GPLv3",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",
    ],
    install_requires=['numpy', 'vtk', 'myPythonLibrary'],
    # python_requires='>=3.6',
)
