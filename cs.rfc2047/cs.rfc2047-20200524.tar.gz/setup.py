#!/usr/bin/env python
from setuptools import setup
setup(
  name = 'cs.rfc2047',
  author = 'Cameron Simpson',
  author_email = 'cs@cskk.id.au',
  version = '20200524',
  url = 'https://bitbucket.org/cameron_simpson/css/commits/all',
  description =
    'unrfc2047: a decoder for RFC2047 (MIME Part 3) encoded text.',
  long_description =
    ('unrfc2047: a decoder for RFC2047 (MIME Part 3) encoded text.\n'    
 '\n'    
 '*Latest release 20200524*:\n'    
 'Handle unknown charsets (parochially and abitrarily) and other decode '    
 'failures.\n'    
 '\n'    
 '## Function `unrfc2047(s)`\n'    
 '\n'    
 'Accept a string `s` containing RFC2047 text encodings (or the whitespace\n'    
 'littered varieties that come from some low quality mail clients) and\n'    
 'decode them into flat Unicode.\n'    
 '\n'    
 'See http://tools.ietf.org/html/rfc2047 for the specification.\n'    
 '\n'    
 '# Release Log\n'    
 '\n'    
 '\n'    
 '\n'    
 '*Release 20200524*:\n'    
 'Handle unknown charsets (parochially and abitrarily) and other decode '    
 'failures.\n'    
 '\n'    
 '*Release 20171231*:\n'    
 'Change final .decode to use "replace". Fix a bunch of warning format '    
 'strings.\n'    
 '\n'    
 '*Release 20170904*:\n'    
 'Initial PyPI release.'),
  classifiers = ['Programming Language :: Python', 'Programming Language :: Python :: 2', 'Programming Language :: Python :: 3', 'Development Status :: 4 - Beta', 'Intended Audience :: Developers', 'Operating System :: OS Independent', 'Topic :: Software Development :: Libraries :: Python Modules', 'License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)'],
  install_requires = ['cs.gimmicks', 'cs.pfx', 'cs.py3'],
  keywords = ['python2', 'python3'],
  license = 'GNU General Public License v3 or later (GPLv3+)',
  long_description_content_type = 'text/markdown',
  package_dir = {'': 'lib/python'},
  py_modules = ['cs.rfc2047'],
)
