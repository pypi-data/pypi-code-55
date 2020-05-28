# -*- coding:utf-8 -*-

import os
from subprocess import call
from .igen import IGen

class VIMDepGen(IGen):

    def generate(self, name):

        call(['pacman', '-Syu'])
        call(['pacman', '-S', 'gvim','python-pip','nodejs', 'npm', 'nerd-fonts-source-code-pro', 'clang', 'gdb'])
        call(['pip', 'install', '--upgrade','pynvim', 'jedi'])
