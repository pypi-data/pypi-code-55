

from setuptools import setup

setup(
    name='cytosim_reader',
    version='0.2.0',
    description='Read data from cytosim simulations to numpy arrays.',
    author='Ilyas Kuhlemann',
    author_email='ilyasp.ku@gmail.com',
    license='GNU GPLv3',
    py_modules=['cytosim_reader'],
    install_requires=['numpy',
                      'pandas']
)
