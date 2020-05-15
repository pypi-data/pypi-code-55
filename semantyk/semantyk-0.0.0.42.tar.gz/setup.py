from setuptools import find_packages, setup
import semantyk

with open('README.md', 'r') as fh:
    long_description = fh.read()

setup(
    author = 'Daniel Bakas Amuchastegui',    
    author_email = 'danielbakas@gmail.com',    
    classifiers = [
        'Development Status :: 1 - Planning',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
    ],
    description = 'Ideas Wonder.',    
    install_requires = ['rdflib'],
    keywords = 'semantyk',
    long_description = long_description,
    long_description_content_type = 'text/markdown',
    maintainer = 'Semantyk',
    name = 'semantyk',
    packages = find_packages(
        exclude = {
            'docs',
            'tests*'
        }
    ),
    url = 'https://github.com/semantykcom/Semantyk',
    version = semantyk.__version__
)