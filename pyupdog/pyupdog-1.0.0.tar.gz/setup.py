import setuptools

with open('readme.md', 'r') as fh:
    long_description = fh.read()

setuptools.setup(
    name='pyupdog',
    version='1.0.0',
    author='Joseph Halstead',
    author_email='josephhalstead89@gmail.com',
    description='Python program for calculating UPD',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/josephhalstead/pyvariantfilter',
    packages=setuptools.find_packages(),
    scripts= ['UPDog.py'],
    classifiers=[
        'Programming Language :: Python :: 3',
        'Operating System :: OS Independent',
    ],
    install_requires=[
   'pysam>=0.15.2',
   'pandas>=0.23.4',
   'seaborn>=0.10.1',
   'scipy>=1.4.1',
   'pyvariantfilter>=1.0.4',
   'numpy>=1.18.1'
],
)