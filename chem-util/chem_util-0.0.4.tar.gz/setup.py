import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="chem_util",
    version="0.0.4",
    author="Robert F. De Jaco",
    author_email="dejac001@umn.edu",
    description="Random Chemistry/Chemical Engineering Utilities",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/dejac001/chem_util",
    packages=['chem_util'],
    python_requires='>=3.6',
    package_dir={'': 'src'},
)
