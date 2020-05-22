import setuptools

with open('README.md', 'r') as fh:
    long_description  =  fh.read()

setuptools.setup(
    name = 'pylinearalgebra',
    version = '0.0.1',
    author = 'Linear Algebra',
    author_email = 'cmstatistics2010@gmail.com',
    description = 'A Linear algebra package',
    long_description = long_description,
    long_description_content_type = 'text/markdown',
    url = 'https://github.com/PyLinearAlgebra/pylinearalgebra',
    packages = setuptools.find_packages(),
    classifiers = [
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires = '>=3.6'
) 