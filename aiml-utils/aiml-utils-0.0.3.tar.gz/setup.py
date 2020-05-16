"""Setup for the aiml-utils package."""

import setuptools


with open('README.md') as f:
    README = f.read()

setuptools.setup(
    author="Pal, Jyoti Prasad",
    author_email="jyotipal.iitkgp@gmail.com",
    name='aiml-utils',
    license="MIT",
    description='aiml-utils is a python package for artificial intelligence and machine learning.',
    version='v0.0.3',
    long_description=README,
    url='https://github.com/jyotiprasadpal/aiml-utils',
    packages=setuptools.find_packages(),
    python_requires=">=3.5",
    install_requires=['requests'],
    classifiers=[
        # Trove classifiers
        # (https://pypi.python.org/pypi?%3Aaction=list_classifiers)
        'Development Status :: 4 - Beta',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Topic :: Software Development :: Libraries',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Intended Audience :: Developers',
    ],
)