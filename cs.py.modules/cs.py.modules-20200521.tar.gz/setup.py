#!/usr/bin/env python
from setuptools import setup
setup(
  name = 'cs.py.modules',
  author = 'Cameron Simpson',
  author_email = 'cs@cskk.id.au',
  version = '20200521',
  url = 'https://bitbucket.org/cameron_simpson/css/commits/all',
  description =
    'Convenience functions related to modules and importing.',
  long_description =
    ('Convenience functions related to modules and importing.\n'    
 '\n'    
 '*Latest release 20200521*:\n'    
 '* New import_module_from_file function to import a Python file as a module '    
 'instance.\n'    
 '* New direct_imports(src_filename,module_name=None) returning the set of '    
 'directly imports module names.\n'    
 '\n'    
 '## Function `direct_imports(src_filename, module_name=None)`\n'    
 '\n'    
 'Crudely parse `src_filename` for `import` statements.\n'    
 'Return the set of directly imported module names.\n'    
 '\n'    
 'If `module_name` is not `None`,\n'    
 'resolve relative imports against it.\n'    
 'Otherwise, relative import names are returned unresolved.\n'    
 '\n'    
 'This is a very simple minded source parse.\n'    
 '\n'    
 '## Function `import_module_from_file(module_name, source_file, '    
 'sys_path=None)`\n'    
 '\n'    
 'Import a specific file as a module instance,\n'    
 'return the module instance.\n'    
 '\n'    
 'Parameters:\n'    
 '* `module_name`: the name to assign to the module\n'    
 '* `source_file`: the source file to load\n'    
 '* `sys_path`: optional list of paths to set as `sys.path`\n'    
 '  for the duration of this import;\n'    
 '  the default is the current value of `sys.path`\n'    
 '\n'    
 'Note that this is a "bare" import;\n'    
 'the module instance is not inserted into `sys.modules`.\n'    
 '\n'    
 '*Warning*: `sys.path` is modified for the duration of this function,\n'    
 'which may affect multithreaded applications.\n'    
 '\n'    
 '## Function `import_module_name(module_name, name, path=None, lock=None)`\n'    
 '\n'    
 'Import `module_name` and return the value of `name` within it.\n'    
 '\n'    
 'Parameters:\n'    
 '* `module_name`: the module name to import.\n'    
 '* `name`: the name within the module whose value is returned;\n'    
 '  if `name` is `None`, return the module itself.\n'    
 '* `path`: an array of paths to use as sys.path during the import.\n'    
 '* `lock`: a lock to hold during the import (recommended).\n'    
 '\n'    
 '## Function `module_attributes(M)`\n'    
 '\n'    
 'Generator yielding the names and values of attributes from a module\n'    
 'which were defined in the module.\n'    
 '\n'    
 '## Function `module_files(M)`\n'    
 '\n'    
 'Generator yielding `.py` pathnames involved in a module.\n'    
 '\n'    
 '## Function `module_names(M)`\n'    
 '\n'    
 'Return a list of the names of attributes from a module which were\n'    
 'defined in the module.\n'    
 '\n'    
 '# Release Log\n'    
 '\n'    
 '\n'    
 '\n'    
 '*Release 20200521*:\n'    
 '* New import_module_from_file function to import a Python file as a module '    
 'instance.\n'    
 '* New direct_imports(src_filename,module_name=None) returning the set of '    
 'directly imports module names.\n'    
 '\n'    
 '*Release 20190101*:\n'    
 'New functions: module_names, module_attributes.\n'    
 '\n'    
 '*Release 20160918*:\n'    
 '* New generator function module_files yielding pathnames.\n'    
 '* import_module_name: accept name=None, just return the module.\n'    
 '* Add empty "install_requires" for DISTINFO completeness.\n'    
 '\n'    
 '*Release 20150116*:\n'    
 'Initial PyPI release.'),
  classifiers = ['Programming Language :: Python', 'Programming Language :: Python :: 2', 'Programming Language :: Python :: 3', 'Development Status :: 4 - Beta', 'Intended Audience :: Developers', 'Operating System :: OS Independent', 'Topic :: Software Development :: Libraries :: Python Modules', 'License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)'],
  install_requires = ['cs.context', 'cs.pfx'],
  keywords = ['python2', 'python3'],
  license = 'GNU General Public License v3 or later (GPLv3+)',
  long_description_content_type = 'text/markdown',
  package_dir = {'': 'lib/python'},
  py_modules = ['cs.py.modules'],
)
