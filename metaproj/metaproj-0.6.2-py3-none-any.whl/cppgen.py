# -*- coding:utf-8 -*-

import os
from .igen import IGen

class CPPGen(IGen):

    def generate(self, name):

        ## Create main path
        ret = self.mkdir(name)
        if not ret: return

        ## Create build path
        build_path = os.path.join(name, 'build')
        self.mkdir(build_path)

        ## Create .root
        dot_root = os.path.join(name, '.root')
        os.mknod(dot_root)

        self.mk_tasks(name)
        self.mk_cmakelists_txt(name)
        self.mk_main_cpp(name)
        self.mk_vimspector(name)

    def mk_vimspector(self, name):
        contents = r'''
{{
  "configurations": {{
    "Debug": {{
      "adapter": "vscode-cpptools",
      "configuration": {{
        "name": "Launch",
        "type": "cppdbg",
        "request": "launch",
        "program": "${{workspaceRoot}}/build/{0}",
        "args": [],
        "cwd": "${{workspaceRoot}}",
        "environment": []
      }}
    }}
  }}
}}'''.format(name)

        filename = os.path.join(name, '.vimspector.json')
        with open(filename, 'w') as f:
            f.write(contents)

    def mk_main_cpp(self, name):

        contents = r'''#include <iostream>

int main(int argc, char *argv[])
{
    std::cout << "Hello, World!" << std::endl;
    return 0;
}'''
        filename = os.path.join(name, 'main.cpp')
        with open(filename, 'w') as f:
            f.write(contents)

    def mk_cmakelists_txt(self, name):

        contents = r'''cmake_minimum_required(VERSION 3.7)

project({0})

add_executable({0} main.cpp)'''.format(name)

        filename = os.path.join(name, 'CMakeLists.txt')
        with open(filename, 'w') as f:
            f.write(contents)

    def mk_tasks(self, name):

        contents = r'''[project-build]
command=cmake --build build
cwd=<root>
errorformat=%f:%l:%m

[project-run]
command="build/$(VIM_PRONAME)"
cwd=<root>
output=terminal'''

        filename = os.path.join(name, '.tasks')
        with open(filename, 'w') as f:
            f.write(contents)


