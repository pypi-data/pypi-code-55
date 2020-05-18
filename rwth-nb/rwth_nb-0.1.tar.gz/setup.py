from setuptools import setup, find_packages

from os import path

here = path.abspath(path.dirname(__file__))

# Get the long description from the README file
with open(path.join(here, 'README.md'), encoding='utf-8') as f:
        long_description = f.read()


setup(name='rwth_nb',
      version='0.1',
      description='RWTH Python Library for Jupyter Notebooks',
      long_description=long_description,
      long_description_content_type='text/markdown',
      url='https://git.rwth-aachen.de/jupyter/rwth-nb',
      author='Christian Rohlfing, Lars Thieling, Christoph Weyer, Jens Schneider, Steffen Vogel',
      author_email='rohlfing@ient.rwth-aachen.de',
      license='MIT',
      packages=find_packages(exclude=['contrib', 'docs', 'tests']),
      install_requires=[], # todo
      zip_safe=False)
