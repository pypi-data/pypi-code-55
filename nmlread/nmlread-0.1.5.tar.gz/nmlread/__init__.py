"Microapp f90nml module wrapper for reading Fortran namelist"

import sys
import os
import io
import f90nml
import shutil
import json

from typing import Any
from microapp import App


class NamelistReader(App):

    _name_ = "nmlread"
    _version_ = "0.1.5"
    _description_ = "Microapp Fortran namelist reader"
    _long_description_ = "Microapp Fortran namelist reader"
    _author_ = "Youngsung Kim"
    _author_email_ = "youngsung.kim.act2@gmail.com"
    _url_ = "https://github.com/grnydawn/micro-nmlread"

    def __init__(self, mgr):

        self.add_argument("namelist", type=str, help="namelist file")
        self.add_argument("-o", "--outfile", type=str, help="file path to namelist in json format")

        self.register_forward("data", type=Any, help="namelist dictionary object")

    def perform(self, args):

        namelist = args.namelist["_"]

        parser = f90nml.Parser()

        if os.path.exists(namelist):
            nml = parser.read(namelist)

        else:
            nml = parser.reads(namelist)

        if args.outfile:

            f90nml.write(nml, args.outfile["_"])
        
        self.add_forward(data=nml.todict(complex_tuple=True))
