import setuptools


setuptools.setup(
    name="OracleSaaSApiPy",
    version="1.0.0.2",
    author="Pratik Munot",
    description="An API wrapper for Oracle SaaS Webservice APIs",
    long_description="An API wrapper for Oracle SaaS Webservice APIs",
    url="https://github.com/pratik-m/OracleERPIntegrationServiceWrapper",
    #package_dir={'':'OracleSaaSApiPy'},
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=['requests'],
    python_requires='>=3.6',
)
