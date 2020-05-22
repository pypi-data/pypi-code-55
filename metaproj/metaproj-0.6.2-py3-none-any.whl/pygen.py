# -*- coding:utf-8 -*-

import os
from .igen import IGen

class PYGen(IGen):

    def generate(self, name):

        ## Create main path
        ret = self.mkdir(name)
        if not ret: return

        ## Create bin path
        bin_path = os.path.join(name, 'tests')
        self.mkdir(bin_path)

        ## Create bin path test.py
        # bin_path_test = os.path.join(name, 'tests/test.py')
        # os.mknod(bin_path_test)

        ## Create .root
        dot_root = os.path.join(name, '.root')
        os.mknod(dot_root)


        ## Create name path
        tail_name = name.split('/')[-1]
        name_path = os.path.join(name, tail_name)
        self.mkdir(name_path)

        ## Create __init__.py
        initpy_path = os.path.join(name_path, '__init__.py')
        os.mknod(initpy_path)

        ## Create README.md
        readme_path = os.path.join(name, 'README.md')
        os.mknod(readme_path)

        # ## Create setup.cfg
        # setupcfg_path = os.path.join(name, 'setup.cfg')
        # os.mknod(setupcfg_path)

        ## Create LICENSE.txt
        license_path = os.path.join(name, 'LICENSE.txt')
        os.mknod(license_path)

        ## Create requirments.txt
        requirments_path = os.path.join(name, 'requirements.txt')
        os.mknod(requirments_path)

        self.mk_install_sh(name)
        self.mk_setup_py(name)
        self.mk_tasks(name)
        self.mk_vimspector(name)
        self.mk_test_py(name)

    def mk_test_py(self, name):
        contents = r'''
# -*- coding: utf-8 -*-
import sys
sys.path.insert(0, '.')

def test():
    pass

if __name__ == "__main__":
    test()'''
        filename = os.path.join(name, 'tests/test.py')
        with open(filename, 'w') as f:
            f.write(contents)

    def mk_vimspector(self, name):
        contents = r'''{
  "configurations": {
    "pdb": {
      "adapter": "debugpy",
      "configuration": {
        "request": "launch",
        "type": "python",
        "cwd": "${workspaceRoot}",
        "program": "${workspaceRoot}/tests/test.py",
        "stopOnEntry": false,
        "console": "integratedTerminal"
      },
      "breakpoints": {
        "exception": {
          "raised": "N",
          "uncaught": ""
        }
      }
    }
  }
} '''

        filename = os.path.join(name, '.vimspector.json')
        with open(filename, 'w') as f:
            f.write(contents)

    def mk_install_sh(self, path):
        contents = r'''#!/bin/bash
python setup.py check
python setup.py bdist_egg --exclude-source-files
python setup.py bdist_wheel
python setup.py install
        '''
        filename = os.path.join(path, 'build.sh')
        with open(filename, 'w') as f:
            f.write(contents)

    def mk_setup_py(self, path):

        proj_name = path.split("/")[-1]
        # -*- coding: utf-8 -*-
        contents = r'''# -*- coding: utf-8 -*-
from setuptools import setup, find_packages

setup(
        name = '{0}',
        version = '0.1',
        description = '',
        long_description = '',
        author='Yizi Wu',
        author_email='wuyz0321@hngytobacco.com',
        packages = find_packages(exclude=['ez_setup', 'tests', 'tests.*', 'bin']),
        license='HNZY',
        include_package_data=True,
        install_requires = [
            ],
        zip_safe = True,
        entry_points={{
            'console_scripts':[
                # 'cmd = {0}.scripts.entry_points:main'
                ]
            }}
        )
        '''.format(proj_name)

        filename = os.path.join(path, 'setup.py')
        with open(filename, 'w') as f:
            f.write(contents)

    def mk_tasks(self, name):

        contents = r'''
[project-build]
command=sudo sh build.sh
cwd=$(VIM_ROOT)
output=terminal

[project-run]
command=python tests/test.py
cwd=<root>
output=terminal
        '''

        filename = os.path.join(name, '.tasks')
        with open(filename, 'w') as f:
            f.write(contents)


