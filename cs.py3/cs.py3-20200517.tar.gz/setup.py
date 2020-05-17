#!/usr/bin/env python
from setuptools import setup
setup(
  name = 'cs.py3',
  author = 'Cameron Simpson',
  author_email = 'cs@cskk.id.au',
  version = '20200517',
  url = 'https://bitbucket.org/cameron_simpson/css/commits/all',
  description =
    'Aids for code sharing between python2 and python3.',
  long_description =
    ('Aids for code sharing between python2 and python3.\n'    
 '\n'    
 '*Latest release 20200517*:\n'    
 'Add date_fromisoformat and datetime_fromisoformat being the datetime.date '    
 'and datetime.datetime isoformat factories.\n'    
 '\n'    
 'This package presents various names in python 3 flavour for common use in\n'    
 'python 2 and python 3.\n'    
 '\n'    
 "## Function `ustr(s, e='utf-8', errors='strict')`\n"    
 '\n'    
 'Upgrade string to unicode: no-op for python 3.\n'    
 '\n'    
 '# Release Log\n'    
 '\n'    
 '\n'    
 '\n'    
 '*Release 20200517*:\n'    
 'Add date_fromisoformat and datetime_fromisoformat being the datetime.date '    
 'and datetime.datetime isoformat factories.\n'    
 '\n'    
 '*Release 20200229*:\n'    
 'Minor fixes.\n'    
 '\n'    
 '*Release 20190729*:\n'    
 'Add DEVNULL, which only arrived with 3.3.\n'    
 '\n'    
 '*Release 20190331*:\n'    
 'cs.py3._for3.raise3: bugfix raise-with-traceback.\n'    
 '\n'    
 '*Release 20190108*:\n'    
 'New raise_from function to provide raise...from in py3 and plain raise in '    
 'py2.\n'    
 '\n'    
 '*Release 20181108*:\n'    
 'Small import fix for pread.\n'    
 '\n'    
 '*Release 20180805*:\n'    
 'Implement pread for systems lacking os.pread.\n'    
 '\n'    
 '*Release 20170903*:\n'    
 '* Make into a package subsuming cs.py3_for2 and cs.py3_for3.\n'    
 '* Implementation of struct.iter_unpack.\n'    
 '* Make bytes.__eq__ work with str for Python 2.\n'    
 '* New name joinbytes for Python 2 and 3.\n'    
 '* Backports for Python 2.5.\n'    
 '\n'    
 '*Release 20160828*:\n'    
 'Use "install_requires" instead of "requires" in DISTINFO.\n'    
 '\n'    
 '*Release 20160827*:\n'    
 '* Move python 2 and 3 specific code into cs.py3_for2 and cs.py3_for3.\n'    
 '* Do not bother with StringIO and BytesIO, modules can get them directly '    
 'from the io module.\n'    
 '* Redo python 2 bytes class.\n'    
 '* Python3 compatible versions of struct.pack and struct.unpack.\n'    
 '\n'    
 '*Release 20150126*:\n'    
 'bugfix py2 ustr()\n'    
 '\n'    
 '*Release 20150120*:\n'    
 'cs.py3: add __contains__ to python 2 bytes type\n'    
 '\n'    
 '*Release 20150112*:\n'    
 'Rerelease with separate README.rst file.\n'    
 '\n'    
 '*Release 20150111*:\n'    
 'ustr: accept errors= parameter, default "strict"; update PyPI distinfo and '    
 'arrangements\n'    
 '\n'    
 '*Release 20150103*:\n'    
 'initial release tag for cs.py3'),
  classifiers = ['Programming Language :: Python', 'Programming Language :: Python :: 2', 'Programming Language :: Python :: 3', 'Development Status :: 4 - Beta', 'Intended Audience :: Developers', 'Operating System :: OS Independent', 'Topic :: Software Development :: Libraries :: Python Modules', 'License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)'],
  install_requires = [],
  keywords = ['python2', 'python3'],
  license = 'GNU General Public License v3 or later (GPLv3+)',
  long_description_content_type = 'text/markdown',
  package_dir = {'': 'lib/python'},
  packages = ['cs.py3'],
)
