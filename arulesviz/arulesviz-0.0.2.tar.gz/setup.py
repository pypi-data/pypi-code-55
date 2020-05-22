from setuptools import setup, find_packages
from os import path

this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='arulesviz',
    use_scm_version=True,
    description='Association Rules visualisation tool',
    long_description=long_description,
    long_description_content_type='text/markdown',
    version='0.0.2',
    url='https://github.com/zveryansky/python-arulesviz',
    author='Alex Zverianskii',
    author_email='',
    license='MIT',
    classifiers=[
    'License :: OSI Approved :: MIT License',

    'Programming Language :: Python :: 3.6',
    'Programming Language :: Python :: 3.7'
    ],
    keywords='association rules graph bqplot arules arulesviz apriori lift slift',
    packages=find_packages(exclude=['examples', 'data']),
    install_requires=['ipywidgets', 'bqplot', 'efficient-apriori'],
)
