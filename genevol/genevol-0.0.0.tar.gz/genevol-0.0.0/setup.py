import codecs
from setuptools import find_packages
from setuptools import setup

install_requires = [
    'cached-property',
    'gym>=0.9.7',
    'numpy>=1.10.4',
    'pillow',
    'scipy',
]

setup(name='genevol',
      version='0.0.0',
      description='Genevol - Genetic and Evolutionary Algorithms',
      long_description=codecs.open('README.md', 'r', encoding='utf-8').read(),
      long_description_content_type='text/markdown',
      author='Prabhat Nagarajan',
      author_email='prabhat@prabhatnagarajan.com',
      license='MIT License',
      packages=find_packages(),
      install_requires=install_requires)