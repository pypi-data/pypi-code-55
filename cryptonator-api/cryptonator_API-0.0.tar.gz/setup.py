from setuptools import setup

from os import path
this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()


setup(name='cryptonator_API',
      version='0.0',
      description='cryptonator_API for https://www.cryptonator.com/',
      packages=['cryptonator_API'],
      author_email='m0rtydisg@gmail.com',
      zip_safe=False,
      long_description=long_description,
      long_description_content_type='text/markdown'
      )