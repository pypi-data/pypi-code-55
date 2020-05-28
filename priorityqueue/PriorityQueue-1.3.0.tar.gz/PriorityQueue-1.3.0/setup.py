import setuptools
from distutils.core import setup
from setuptools import setup

"""with open("README.md", "r") as fh:
    long_description = fh.read()"""

setup(
  name = 'PriorityQueue',         # How you named your package folder (MyLib)
  version='1.3.0',
  #packages = ['PriorityQueue'],   # Chose the same as "name"
        # Start with a small number and increase it with every change you make
  license='MIT',        # Chose a license from here: https://help.github.com/articles/licensing-a-repository
  description = 'Prioroty Heap package which can perform priorirty queue operations on Objects or on Primitive data type objects like int and float',   # Give a short description about your library
  author = 'Sandeep Palagati',                   # Type in your name
  author_email = 'palagati.s@gmail.com',      # Type in your E-Mail
  url = 'https://github.com/sandeepPalagati/PriorityQueue',   # Provide either the link to your github or to your website
  download_url = 'https://github.com/user/reponame/archive/v_01.tar.gz',    # I explain this later on
  classifiers=[
    'Development Status :: 3 - Alpha',      # Chose either "3 - Alpha", "4 - Beta" or "5 - Production/Stable" as the current state of your package
    'Intended Audience :: Developers',      # Define that your audience are developers
    'Topic :: Software Development :: Build Tools',
    'License :: OSI Approved :: MIT License',   # Again, pick a license
    'Programming Language :: Python :: 3',      #Specify which pyhton versions that you want to support
    'Programming Language :: Python :: 3.4',
    'Programming Language :: Python :: 3.5',
    'Programming Language :: Python :: 3.6',
    'Operating System :: OS Independent',
  ],
)
