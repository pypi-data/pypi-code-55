
from setuptools import setup

with open('README.md', encoding='utf-8') as f:
    long_description = f.read()

setup(name = 'Multiple_dummies',
      
      version = '2.0',
      
      description = long_description,
      
      packages = ['Multiple_dummies'],
      
      author = 'Rajath Nagaraj',
      
      author_email= 'rnagara1@mtu.edu',
      
      zip_safe=False)