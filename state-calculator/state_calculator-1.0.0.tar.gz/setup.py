from setuptools import setup, find_packages

setup(
    name='state_calculator',
    version='1.0.0',
    packages=find_packages(),
    install_requires=[
          'selenium',
          'pandas',
          'lxml',
      ],
    url='',
    include_package_data=True,
    license='MIT',
    author='Victor Athanasio',
    author_email='victorathanasio@usp.br',
    description=''
)
