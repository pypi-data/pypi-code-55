from setuptools import setup, find_packages
from nfiparcel import __version__


long_description = ''
with open('./README.md') as f:
    long_description = f.read()

install_requires = []
with open('./requirements.txt') as f:
    install_requires = f.read().splitlines()

setup(name='nfiparcel',
    version=__version__,
    description='Python package for parcel analysis and rating.',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url='https://github.com/NFI-Industries/nfiparcel',
    author='Chris Pryer',
    author_email='chris.pryer@nfiindustries.com',
    license='PUBLIC',
    packages=find_packages(),
    install_requires=install_requires,
    entry_points ={ 
            'console_scripts': [ 
                'nfiparcel = nfiparcel:clientry'
            ] 
        },
    zip_safe=False)