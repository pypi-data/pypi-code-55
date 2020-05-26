from setuptools import setup
import logger

setup(
    name=logger.__title__,
    version=logger.__version__,
    packages=['logger'],
    install_requires=['colorama', 'cursor'],
    url='https://github.com/Dest0re/Dest0res-logger',
    license='',
    author='Dest0re',
    author_email='dest0re.louisell@gmail.com',
    description=''
)
