from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()
        
setup(
    name='GPACalculator',
    version='0.0.1',
    description='Calculator for GPA',
    url='https://github.com/s-callahan/GPACalculator',
    author='s-callahan',
    author_email='callasha000@gmail.com',
    package_dir={'': 'src'},
    py_modules=["GPACalculator"],
    long_description=long_description,
    long_description_content_type="text/markdown",
)
