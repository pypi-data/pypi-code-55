import setuptools
import vs301_util

# read the contents of your README file
from os import path
this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

with open('requirements.txt') as f:
    required = f.read().splitlines()


    
setuptools.setup(
    name="vs301_util",
    version=vs301_util.__version__,

    author="mrzjo",
    author_email="mrzjo05@gmail.com",
    url="https://gitlab.com/telelian/peripheral-library/vs301-systemutil",

    description="vs301 utils",
    long_description=long_description,
    long_description_content_type='text/markdown',
    
    packages=setuptools.find_packages(),

    install_requires=required,

    classifiers=[
        'Development Status :: 4 - Beta',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Topic :: System :: Hardware'
    ],
)
