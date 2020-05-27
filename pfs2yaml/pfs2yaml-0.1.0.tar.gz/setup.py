import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="pfs2yaml",
    version="0.1.0",
    install_requires=["pyyaml", "click"],
    author="Henrik Andersson",
    author_email="jan@dhigroup.com",
    description="A package that can convert DHI pfs files to yaml",
    platform="windows_x64",
    license="MIT",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/DHI/pypfs2yaml",
    packages=setuptools.find_packages(),
    classifiers=[
        "License :: OSI Approved :: BSD License",
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Science/Research",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Operating System :: Microsoft :: Windows",
        "Topic :: Scientific/Engineering",
    ],
    entry_points="""
        [console_scripts]
        pfs2yaml=pfs2yaml.cli:cli
    """,
)
