import os
from .pygen import PYGen
from .cppgen import CPPGen
from .vimgen import VIMGen
from .vimdepgen import VIMDepGen

class MetaProj:

    def __init__(self, name='demo', projtype='python'):
        self.name = name
        self.projtype = projtype

    def run(self):

        if self.projtype == 'python':
            PYGen().generate(self.name)
        elif self.projtype == 'cpp':
            CPPGen().generate(self.name)
        elif self.projtype == 'vim':
            VIMGen().generate(self.name)
        elif self.projtype == 'vimdep':
            VIMDepGen().generate(self.name)
        else:
            print("MetaProj: Unknown Project Type")

    def setName(self, name):
        self.name = name

    def setType(self, projtype):
        self.projtype = projtype
