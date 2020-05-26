"""
squeue: A simple SQLite Queue
"""
from setuptools import setup, find_packages

VERSION = '1.2'

setup(name='squeue',
      version=VERSION,
      description="squeue: A simple SQLite Queue",
      long_description="A Job Queue implementation using SQLite",
      classifiers=['Topic :: System :: Distributed Computing'],
      keywords='sqlite queue job workflow',
      author='Karthik Kumar Viswanathan',
      author_email='karthikkumar@gmail.com',
      url='https://github.com/guilt/squeue',
      license='BSD',
      packages=find_packages(exclude=['ez_setup', 'examples', 'tests']),
      include_package_data=True,
      zip_safe=True,
      install_requires=[],
     )
