#!/usr/bin/env python
from setuptools import setup
setup(
  name = 'cs.context',
  author = 'Cameron Simpson',
  author_email = 'cs@cskk.id.au',
  version = '20200517',
  url = 'https://bitbucket.org/cameron_simpson/css/commits/all',
  description =
    'Context managers. Initially just `stackattrs`.',
  long_description =
    ('Context managers. Initially just `stackattrs`.\n'    
 '\n'    
 '*Latest release 20200517*:\n'    
 '* Add `nullcontext` like the one from recent contextlib.\n'    
 '* stackattrs: expose the push and pop parts as pushattrs() and popattrs().\n'    
 '\n'    
 '## Function `popattrs(o, attr_names, old_values)`\n'    
 '\n'    
 'The "pop" part of stackattrs.\n'    
 'Restore previous attributes of `o`\n'    
 'named by `attr_names` with previous state in `old_values`.\n'    
 '\n'    
 '## Function `pushattrs(o, **attr_values)`\n'    
 '\n'    
 'The "push" part of stackattrs.\n'    
 'Push `attr_values` onto `o` as attributes,\n'    
 'return the previous attribute values in a dict.\n'    
 '\n'    
 '## Function `stackattrs(o, **attr_values)`\n'    
 '\n'    
 'Context manager to push new values for the attributes of `o`\n'    
 'and to restore them afterward.\n'    
 'Returns a `dict` containing a mapping of the previous attribute values.\n'    
 'Attributes not present are not present in the mapping.\n'    
 '\n'    
 'Restoration includes deleting attributes which were not present\n'    
 'initially.\n'    
 '\n'    
 'Example of fiddling a programme\'s "verbose" mode:\n'    
 '\n'    
 '    >>> class RunModes:\n'    
 '    ...     def __init__(self, verbose=False):\n'    
 '    ...         self.verbose = verbose\n'    
 '    ...\n'    
 '    >>> runmode = RunModes()\n'    
 '    >>> if runmode.verbose:\n'    
 '    ...     print("suppressed message")\n'    
 '    ...\n'    
 '    >>> with stackattrs(runmode, verbose=True):\n'    
 '    ...     if runmode.verbose:\n'    
 '    ...         print("revealed message")\n'    
 '    ...\n'    
 '    revealed message\n'    
 '    >>> if runmode.verbose:\n'    
 '    ...     print("another suppressed message")\n'    
 '    ...\n'    
 '\n'    
 'Example exhibiting restoration of absent attributes:\n'    
 '\n'    
 '    >>> class O:\n'    
 '    ...     def __init__(self):\n'    
 '    ...         self.a = 1\n'    
 '    ...\n'    
 '    >>> o = O()\n'    
 '    >>> print(o.a)\n'    
 '    1\n'    
 '    >>> print(o.b)\n'    
 '    Traceback (most recent call last):\n'    
 '      File "<stdin>", line 1, in <module>\n'    
 "    AttributeError: 'O' object has no attribute 'b'\n"    
 '    >>> with stackattrs(o, a=3, b=4):\n'    
 '    ...     print(o.a)\n'    
 '    ...     print(o.b)\n'    
 '    ...     o.b = 5\n'    
 '    ...     print(o.b)\n'    
 "    ...     delattr(o, 'a')\n"    
 '    ...\n'    
 '    3\n'    
 '    4\n'    
 '    5\n'    
 '    >>> print(o.a)\n'    
 '    1\n'    
 '    >>> print(o.b)\n'    
 '    Traceback (most recent call last):\n'    
 '      File "<stdin>", line 1, in <module>\n'    
 "    AttributeError: 'O' object has no attribute 'b'\n"    
 '\n'    
 '# Release Log\n'    
 '\n'    
 '\n'    
 '\n'    
 '*Release 20200517*:\n'    
 '* Add `nullcontext` like the one from recent contextlib.\n'    
 '* stackattrs: expose the push and pop parts as pushattrs() and popattrs().\n'    
 '\n'    
 '*Release 20200228.1*:\n'    
 'Initial release with stackattrs context manager.'),
  classifiers = ['Programming Language :: Python', 'Programming Language :: Python :: 2', 'Programming Language :: Python :: 3', 'Development Status :: 4 - Beta', 'Intended Audience :: Developers', 'Operating System :: OS Independent', 'Topic :: Software Development :: Libraries :: Python Modules', 'License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)'],
  install_requires = [],
  keywords = ['python2', 'python3'],
  license = 'GNU General Public License v3 or later (GPLv3+)',
  long_description_content_type = 'text/markdown',
  package_dir = {'': 'lib/python'},
  py_modules = ['cs.context'],
)
