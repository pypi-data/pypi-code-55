from setuptools import find_packages, setup
setup(
   name='covid19_csv', ## Este nombre debe ser único y no estar indexado
   version='0.2',
   packages=find_packages(),
   py_modules=['covid19_csv'] ## Este debe ser el nombre del archivo *.py
)   