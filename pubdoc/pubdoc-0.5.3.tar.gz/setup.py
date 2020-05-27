from setuptools import setup, find_packages
from os import path
from io import open
from pubdoc.__version__ import __version__

here_path = path.abspath(path.dirname(__file__))

# Get the long description from the README file
with open(path.join(here_path, 'readme.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(name='pubdoc',
      python_requires='>=3.6.0',
      version=__version__,
      description='Make technical documentstion from data sets',
      long_description=long_description,
      long_description_content_type='text/markdown',
      author='Evgenii Alaev',
      author_email='ev.alaev@yandex.ru',
      url='https://github.com/brobots-corporation/pubdoc',
      license='GPL-3.0',
      classifiers=[
          'Development Status :: 4 - Beta',
          'Intended Audience :: Developers',
          'Natural Language :: Russian',
          'Operating System :: OS Independent',
          'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
          'Programming Language :: Python :: 3.6',
          'Programming Language :: Python :: 3.7',
          'Programming Language :: Python :: 3.8',
          'Topic :: Software Development :: Libraries :: Python Modules'
      ],
      install_requires=[
            'Click>=7.0',
            'dokuwiki==1.2.1',
            'pprint==0.1',
        ],
      packages=find_packages(),
      #tests_require=['coverage', 'unittest-xml-reporting'],
      #test_suite='tests',
      entry_points={
          'console_scripts': [
              'pubdoc=pubdoc.app:run'
          ]
      },
      project_urls={
          'Bug Reports': 'https://github.com/brobots-corporation/pubdoc/issues',
          'Source': 'https://github.com/brobots-corporation/pubdoc',
      }
      )