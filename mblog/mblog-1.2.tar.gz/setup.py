"""
mblog: a minimal markdown blog
"""
from setuptools import setup, find_packages

VERSION = '1.2'

def get_requirements():
    with open('requirements.txt') as requirements:
        for req in requirements:
            req = req.strip()
            if req and not req.startswith('#'):
                yield req


def get_readme():
    with open('README.md') as readme:
            return readme.read()

setup(name='mblog',
      version=VERSION,
      description="mblog: a minimal markdown blog",
      long_description=get_readme(),
      long_description_content_type='text/markdown',
      classifiers=['Topic :: Internet :: WWW/HTTP :: Dynamic Content :: Content Management System'],
      keywords='blog markdown flask minimal',
      author='Karthik Kumar Viswanathan',
      author_email='karthikkumar@gmail.com',
      url='https://github.com/guilt/mblog',
      license='BSD',
      packages=find_packages(exclude=['ez_setup', 'examples', 'examples.*', 'tests']),
      include_package_data=True,
      zip_safe=False,
      scripts=['scripts/mblog'],
      install_requires=list(get_requirements()),
     )
