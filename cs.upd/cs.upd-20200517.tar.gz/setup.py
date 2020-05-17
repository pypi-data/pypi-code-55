#!/usr/bin/env python
from setuptools import setup
setup(
  name = 'cs.upd',
  author = 'Cameron Simpson',
  author_email = 'cs@cskk.id.au',
  version = '20200517',
  url = 'https://bitbucket.org/cameron_simpson/css/commits/all',
  description =
    'Single line status updates with minimal update sequences.',
  long_description =
    ('Single line status updates with minimal update sequences.\n'    
 '\n'    
 '*Latest release 20200517*:\n'    
 '* Multiline support!\n'    
 '* Multiline support!\n'    
 '* Multiline support!\n'    
 '* New UpdProxy class to track a status line of a multiline Upd in the face '    
 'of further inserts and deletes.\n'    
 '* Upd(...) now returns a context manager to clean up the display on its '    
 'exit.\n'    
 '* Upd(...) is now a SingletonMixin in order to use the same state if set up '    
 'in multiple places.\n'    
 '\n'    
 'This is available as an output mode in `cs.logutils`.\n'    
 '\n'    
 'Example:\n'    
 '\n'    
 '    with Upd() as U:\n'    
 '        for filename in filenames:\n'    
 '            U.out(filename)\n'    
 '            ... process filename ...\n'    
 "            upd.nl('an informational line')\n"    
 '\n'    
 '## Function `cleanupAtExit()`\n'    
 '\n'    
 'Cleanup function called at programme exit to clear the status line.\n'    
 '\n'    
 '## Class `Upd(cs.obj.SingletonMixin)`\n'    
 '\n'    
 'A `SingletonMixin` subclass for maintaining a regularly updated status '    
 'line.\n'    
 '\n'    
 '## Class `UpdProxy`\n'    
 '\n'    
 'A proxy for a status line of a multiline `Upd`.\n'    
 '\n'    
 'This provides a stable reference to a status line after it has been\n'    
 'instantiated by `Upd.insert`.\n'    
 '\n'    
 'The status line can be accessed and set via the `.text` property.\n'    
 '\n'    
 '# Release Log\n'    
 '\n'    
 '\n'    
 '\n'    
 '*Release 20200517*:\n'    
 '* Multiline support!\n'    
 '* Multiline support!\n'    
 '* Multiline support!\n'    
 '* New UpdProxy class to track a status line of a multiline Upd in the face '    
 'of further inserts and deletes.\n'    
 '* Upd(...) now returns a context manager to clean up the display on its '    
 'exit.\n'    
 '* Upd(...) is now a SingletonMixin in order to use the same state if set up '    
 'in multiple places.\n'    
 '\n'    
 '*Release 20200229*:\n'    
 '* Upd: can now be used as a context manager, clearing the line on exit.\n'    
 '* Upd.without is now a context manager, returning the older state, and '    
 'accepting an optional inner state (default "").\n'    
 '* Upd is now a singleton factory, obsoleting upd_for.\n'    
 '* Upd.nl: use "insert line above" mode if supported.\n'    
 '\n'    
 '*Release 20181108*:\n'    
 'Documentation improvements.\n'    
 '\n'    
 '*Release 20170903*:\n'    
 '* New function upd_for(stream) returning singleton Upds.\n'    
 '* Drop noStrip keyword argument/mode - always strip trailing whitespace.\n'    
 '\n'    
 '*Release 20160828*:\n'    
 '* Use "install_requires" instead of "requires" in DISTINFO.\n'    
 '* Add Upd.flush method.\n'    
 '* Upd.out: fix longstanding trailing text erasure bug.\n'    
 '* Upd.nl,out: accept optional positional parameters, use with %-formatting '    
 'if supplied, just like logging.\n'    
 '\n'    
 '*Release 20150118*:\n'    
 'metadata fix\n'    
 '\n'    
 '*Release 20150116*:\n'    
 'Initial PyPI release.'),
  classifiers = ['Programming Language :: Python', 'Programming Language :: Python :: 2', 'Programming Language :: Python :: 3', 'Development Status :: 4 - Beta', 'Intended Audience :: Developers', 'Operating System :: OS Independent', 'Topic :: Software Development :: Libraries :: Python Modules', 'License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)'],
  install_requires = ['cs.gimmicks', 'cs.lex', 'cs.obj', 'cs.tty'],
  keywords = ['python2', 'python3'],
  license = 'GNU General Public License v3 or later (GPLv3+)',
  long_description_content_type = 'text/markdown',
  package_dir = {'': 'lib/python'},
  py_modules = ['cs.upd'],
)
