from setuptools import setup, find_packages

setup(
   name='va-timeseries',
   version='1.0.1',
   description='Timeseries Analysis',
   author='Joocer',
   author_email='justin.joyce@joocer.com',
   packages=find_packages(),
   install_requires=['pandas', 'matplotlib', 'numpy']
)