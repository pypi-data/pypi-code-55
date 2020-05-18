from setuptools import setup, find_packages

with open('README.md', 'r') as fh:
    long_description = fh.read()

setup(
    name='pygarch',
    version="0.0.2",
    author="Oliver Chambers",
    long_description=long_description,
    url='https://gitlab.corp.vesparum.com/oliver.chambers/pygarch',
    packages=find_packages(),
    package_data={'pygarch': ['lib/*.R']},
    install_requires=[
        "pandas",
        "rpy2<3"
    ],
    classifiers=[
        "Programming Language :: Python :: 3.6",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        'Topic :: Utilities',
    ],
)
