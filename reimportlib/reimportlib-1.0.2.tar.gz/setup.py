"""
reimportlib: refactored imports
"""
from setuptools import setup, find_packages

VERSION = '1.0.2'


def get_requirements():
    with open('requirements.txt') as requirements:
        for req in requirements:
            req = req.strip()
            if req and not req.startswith('#'):
                yield req


def get_readme():
    with open('README.md') as readme:
        return readme.read()


setup(name='reimportlib',
      version=VERSION,
      description="reimportlib: refactored imports",
      long_description=get_readme(),
      long_description_content_type='text/markdown',
      classifiers=['Topic :: Software Development :: Libraries :: Python Modules'],
      keywords='importlib refactor module rename move serialize',
      author='Karthik Kumar Viswanathan',
      author_email='karthikkumar@gmail.com',
      url='https://github.com/guilt/reimportlib',
      license='BSD',
      packages=find_packages(exclude=['ez_setup', 'examples', 'examples.*', 'tests']),
      include_package_data=False,
      zip_safe=True,
      install_requires=list(get_requirements()),
     )
