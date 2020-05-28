#!/usr/bin/env python3
"""
setup.py file for StructuredData.

See http://docs.python.org/install
on how to use setup.py
"""

# pylint: disable= invalid-name

#from distutils.core import setup
from setuptools import setup, find_packages

import os
import os.path
import sys
import shutil
import subprocess

__version__="5.1" #VERSION#

if sys.version_info[0] < 3:
    sys.exit("error: python 3 or newer is required for this application")

base_name= 'python3'

# data ------------------------------

dependencies= { "pypi": ["PyYAML"],
                "rpm" : ["python3-pyyaml","python3-tkinter","tix"],
                "deb" : ["libyaml-0-2","python3-yaml","python3-tk","tix"]
              }

# utilities -------------------------

def readme_rst():
    """return contents of README.rst file."""
    # taken from:
    # https://packaging.python.org/guides/making-a-pypi-friendly-readme/
    this_directory = os.path.abspath(os.path.dirname(__file__))
    with open(os.path.join(this_directory, 'README.rst'),
              encoding='utf-8') as f:
        long_description = f.read()
    return long_description

def find_files(path):
    """find files and directories below a given path.

    here is an example of the returned data structure:
    {'doc/_build/html': ['objects.inv', 'searchindex.js', 'index.html'],
     'doc/_build': [],
     'doc/_build/html/_sources': ['license.txt', 'index.txt']
     'doc/_build/doctrees': ['SDpyshell.doctree', 'license.doctree']
    }
    """
    paths= {}
    for dirpath, _, filenames in os.walk(path):
        paths[dirpath]= filenames
    return paths

def pathsplit(path):
    """splits a path into pieces.

    Here are some examples:
    >>> pathsplit("A")
    ['A']
    >>> pathsplit("A/B")
    ['A', 'B']
    >>> pathsplit("A/B/C")
    ['A', 'B', 'C']
    >>> pathsplit("A/B.x/C.y")
    ['A', 'B.x', 'C.y']
    """
    l= []
    while True:
        (head,tail)=os.path.split(path)
        l.append(tail)
        if not head:
            break
        path= head
    l.reverse()
    return l

def path_rebase(path, base):
    """rebases a path.

    Here are some examples:
    >>> path_rebase("doc/_build/html/_sources","doc/_build")
    'html/_sources'
    >>> path_rebase("doc/_build/html/_sources","doc/_build/html")
    '_sources'
    >>> path_rebase("doc/_build/html/_sources","doc")
    '_build/html/_sources'
    >>> path_rebase("doc/_build/html/_sources","doc/_bduild")
    'doc/_build/html/_sources'
    """
    path_l= pathsplit(path)
    base_l= pathsplit(base)
    if len(path_l)<len(base_l):
        return path
    # pylint: disable= consider-using-enumerate
    for i in range(len(base_l)):
        if base_l[i]!=path_l[i]:
            return path
    if len(path_l)==len(base_l):
        return ""
    return os.path.join(*path_l[len(base_l):])

def data_statements(install_path, source_path):
    """create data statements for arbitrary files."""
    filedict= find_files(source_path)
    data_dict= {}
    for (path,files) in list(filedict.items()):
        subdir= path_rebase(path, source_path)
        if subdir != "":
            destpath= os.path.join(install_path, subdir)
        else:
            destpath= install_path
        for f in files:
            l= data_dict.get(destpath)
            if l is None:
                l= []
                data_dict[destpath]= l
            l.append(os.path.join(path, f))
    return list(data_dict.items())

def copy_files(dest_dir, source_dir, source_files):
    """copy files from source to dest if they are newer.
    """
    if not os.path.exists(dest_dir):
        os.mkdir(dest_dir)
    for f in source_files:
        src= os.path.join(source_dir,f)
        dst= os.path.join(dest_dir, f)
        if os.path.exists(dst):
            if os.path.getmtime(dst)>=os.path.getmtime(src):
                continue
        shutil.copyfile(src, dst)

# main      -------------------------

doc_install_dir= os.path.join("share","doc","StructuredData-%s" % __version__)
html_install_dir= os.path.join(doc_install_dir, "html")

doc_dir= "doc"

html_build_dir= os.path.join(doc_dir,"_build","html")

data_doc_dir= os.path.join("StructuredData","data")

# create HTML documentation if it doesn't already exist:
if not os.path.exists(html_build_dir):
    # "make -C doc html":
    subprocess.check_call(["make", "-C", "doc", "html"])

# create files in data directory
copy_files(data_doc_dir, doc_dir, ["SDpyshell.rst"])

data_files_list= [(doc_install_dir, ["README.rst", "LICENSE"])]

# add all generated html documentation to data_files_list:
data_files_list.extend(data_statements(html_install_dir, html_build_dir))

name='yaml-structureddata'

if "deps-pypi" in sys.argv:
    print(",".join(dependencies["pypi"]))
    sys.exit(0)
if "deps-rpm" in sys.argv:
    print(",".join(dependencies["rpm"]))
    sys.exit(0)
if "deps-deb" in sys.argv:
    print(",".join(dependencies["deb"]))
    sys.exit(0)

if "bdist_rpm" in sys.argv:
    name= base_name+"-"+name

setup(name=name,
      version= __version__,
      packages=['StructuredData','StructuredData.internal'],
      #packages=['StructuredData'],
      #package_dir= {'': 'StructuredData'},
      scripts=['bin/SDpyshell','bin/SDxmlrpc','bin/SDview'],

      package_data={'StructuredData': ['data/*']},
      data_files= data_files_list,

      python_requires= ">=3.2.3",
      install_requires= dependencies["pypi"],
      zipsafe= True,

      author='Goetz Pfeiffer',
      author_email='Goetz.Pfeiffer@helmholtz-berlin.de',
      description='A YAML based database with types.',
      long_description= readme_rst(),
      long_description_content_type= 'text/x-rst',
      url='https://yaml-structureddata.sourceforge.io',
      download_url='https://sourceforge.net/projects/yaml-structureddata/files/?source=navbar',
      classifiers=[
          'Development Status :: 6 - Mature',
          'Environment :: Console',
          'Intended Audience :: Developers',
          'Intended Audience :: Information Technology',
          'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
          'Natural Language :: English',
          'Operating System :: OS Independent',
          'Operating System :: POSIX',
          'Operating System :: Unix',
          'Operating System :: POSIX :: Linux',
          'Programming Language :: Python :: 3',
          'Programming Language :: Python :: 3.2',
          'Programming Language :: Python :: 3.3',
          'Programming Language :: Python :: 3.4',
          'Programming Language :: Python :: 3.5',
          'Programming Language :: Python :: 3.6',
          'Programming Language :: Python :: 3.7',
          'Topic :: Database',
          'Topic :: Database :: Database Engines/Servers',
          'Topic :: Software Development :: Libraries :: Python Modules',
          ],
      license= "GPLv3",
     )

