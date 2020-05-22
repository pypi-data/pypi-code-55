from setuptools import setup, find_packages
# based on mocanexion by @rnsaway

setup(
    name='mocanexion2',
    version='0.4',
    packages=find_packages(exclude=['contrib', 'docs', 'tests']),
    url='https://github.com/Hittwar/mocanexion2',
    license='The Unlicense',
    author='Hittwar',
    author_email='hittwar@hotmail.com',
    description='Python connection to MOCA-WMS 2017 - 2018 - 2019 - 2020',
    keywords='moca wms',
    install_requires=['pandas', 'requests'],
    python_requires='>=3'
)