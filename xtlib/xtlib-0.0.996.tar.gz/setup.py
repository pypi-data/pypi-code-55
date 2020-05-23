import setuptools

# supply contents of our README file as our package's long description
with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    # this is the name people will use to "pip install" the package
    name="xtlib",

    # this must be incremented every time we push an update to pypi
    version="0.0.996",

    author="Roland Fernandez",
    author_email="rfernand@microsoft.com",
    description="A set of tools for organizing and scaling ML experiments",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/rfernand2",

    # this will find our package "xtlib" by its having an "__init__.py" file
    packages=["xtlib", "xtlib.helpers"],   # setuptools.find_packages(),

    # this will be copied to a directory on the PATH
    scripts=[
        'scripts/xt.bat', 
        'scripts/xt',
        'scripts/run_xt.py'
    ],

    # normally, only *.py files are included - this forces our TOML file to be included
    package_data={'': ['default_config.toml']},
    include_package_data=True,   

    # the packages that our package is dependent on
    install_requires=[
        "azure-storage-file==2.0.1",
        "azure-storage-blob==2.0.1", 
        "azure-batch==6.0.0", 
        "numpy", 
        "arrow==0.14.0",    # avoid annoying warning msgs in 0.14.4, 
        "toml",
        "psutil",
        # rpyc requires its versions to match (client/remote)
        "rpyc==4.1.0",
        "matplotlib",
        # windows only packages
        "pywin32; platform_system == 'Windows'",
        "tqdm",
    ],

    # used to identify the package to various searches
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
