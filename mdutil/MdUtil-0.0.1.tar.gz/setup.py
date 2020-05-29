import setuptools

setuptools.setup(
    name='MdUtil',  # ? Package name
    version="0.0.1",  # ? Package version
    description="Markdown utility for python",  # ? Package description
    # ? Package's long description (visible on PyPi)
    long_description=open("README.md").read(),
    # ? Long description's content type
    long_description_content_type="text/markdown",
    # ? Package url (usually github and visible on PyPi)
    url="https://github.com/Theodore-Robinson/MdUtil",
    packages=setuptools.find_packages(),  # ? Packages
    package_dir={'': 'src'},  # ? Package directory
    # ? Package modules (things provided to the installer. Taken from package_dir)
    py_modules=['parsemd'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent"
    ],  # ? Package classifiers
    install_requires=[],  # ? Package dependencies (requests etc)
    extras_require={
        "dev": [
            "autopep8",
            "flake8"
        ]
    }
)
