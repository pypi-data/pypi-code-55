import setuptools

setuptools.setup(
    name="myVTKPythonLibrary",
    version="2020.05.22",
    author="Martin Genet",
    author_email="martin.genet@polytechnique.edu",
    description="A collection of tools to manipulate meshes and images using vtkpython",
    long_description = open("README.md", "r").read(),
    long_description_content_type="text/markdown",
    url="https://gitlab.inria.fr/mgenet/myVTKPythonLibrary",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",
    ],
    install_requires=['numpy', 'vtk', 'myPythonLibrary'],
    # python_requires='>=3.6',
)
