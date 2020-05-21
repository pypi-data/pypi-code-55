#!/usr/bin/env python
from setuptools import setup
setup(
  name = 'cs.tty',
  author = 'Cameron Simpson',
  author_email = 'cs@cskk.id.au',
  version = '20200521',
  url = 'https://bitbucket.org/cameron_simpson/css/commits/all',
  description =
    'Functions related to terminals.',
  long_description =
    ('Functions related to terminals.\n'    
 '\n'    
 '*Latest release 20200521*:\n'    
 '* New status() function dragged in from cs.logutils, which uses cs.upd for '    
 'status() -- needs some refactoring to match with the other functions in '    
 'cs.tty -- text vs bytes, stdout vs stderr, etc.\n'    
 '* Get warning() from cs.gimmicks.\n'    
 '\n'    
 '## Function `setupterm(*args)`\n'    
 '\n'    
 'Run curses.setupterm, needed to be able to use the status line.\n'    
 'Uses a global flag to avoid doing this twice.\n'    
 '\n'    
 '## Function `status(msg, *args, **kwargs)`\n'    
 '\n'    
 "Write a message to the terminal's status line.\n"    
 '\n'    
 'Parameters:\n'    
 '* `msg`: message string\n'    
 '* `args`: if not empty, the message is %-formatted with `args`\n'    
 '* `file`: optional keyword argument specifying the output file.\n'    
 '  Default: `sys.stderr`.\n'    
 '\n'    
 'Hack: if there is no status line use the xterm title bar sequence :-(\n'    
 '\n'    
 '## Function `statusline(text, fd=None, reverse=False, xpos=None, '    
 'ypos=None)`\n'    
 '\n'    
 'Update the status line.\n'    
 '\n'    
 '## Function `statusline_bs(text, reverse=False, xpos=None, ypos=None)`\n'    
 '\n'    
 'Return a byte string to update the status line.\n'    
 '\n'    
 '## Function `ttysize(fd)`\n'    
 '\n'    
 'Return a (rows, columns) tuple for the specified file descriptor.\n'    
 '\n'    
 'If the window size cannot be determined, None will be returned\n'    
 'for either or both of rows and columns.\n'    
 '\n'    
 'This function relies on the UNIX `stty` command.\n'    
 '\n'    
 '## Class `WinSize(builtins.tuple)`\n'    
 '\n'    
 'WinSize(rows, columns)\n'    
 '\n'    
 '# Release Log\n'    
 '\n'    
 '\n'    
 '\n'    
 '*Release 20200521*:\n'    
 '* New status() function dragged in from cs.logutils, which uses cs.upd for '    
 'status() -- needs some refactoring to match with the other functions in '    
 'cs.tty -- text vs bytes, stdout vs stderr, etc.\n'    
 '* Get warning() from cs.gimmicks.\n'    
 '\n'    
 '*Release 20190101*:\n'    
 'Small bugfix for setupterm.\n'    
 '\n'    
 '*Release 20170903*:\n'    
 'add statusline and statusline_s functions; ttysize: support BSD stty output '    
 'format\n'    
 '\n'    
 '*Release 20160828*:\n'    
 'Use "install_requires" instead of "requires" in DISTINFO, add PyPI '    
 'category.\n'    
 '\n'    
 '*Release 20150116*:\n'    
 'Initial PyPI release.'),
  classifiers = ['Environment :: Console', 'Operating System :: POSIX', 'Programming Language :: Python', 'Programming Language :: Python :: 2', 'Programming Language :: Python :: 3', 'Topic :: Terminals', 'Development Status :: 4 - Beta', 'Intended Audience :: Developers', 'License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)'],
  install_requires = ['cs.gimmicks'],
  keywords = ['python2', 'python3'],
  license = 'GNU General Public License v3 or later (GPLv3+)',
  long_description_content_type = 'text/markdown',
  package_dir = {'': 'lib/python'},
  py_modules = ['cs.tty'],
)
