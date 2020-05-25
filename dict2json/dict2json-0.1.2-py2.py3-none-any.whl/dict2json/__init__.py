"Microapp f90nml module wrapper for reading Fortran namelist"

import sys
import os
import io
import shutil
import json

from typing import Any
from microapp import App


class Dict2Json(App):

    _name_ = "dict2json"
    _version_ = "0.1.2"
    _description_ = "Microapp convertor from Python dictionary to Json"
    _long_description_ = "Microapp convertor from Python dictionary to Json"
    _author_ = "Youngsung Kim"
    _author_email_ = "youngsung.kim.act2@gmail.com"
    _url_ = "https://github.com/grnydawn/micro-dict2json"

    def __init__(self, mgr):

        self.add_argument("data", help="dictionary data")
        self.add_argument("-o", "--outfile", type=str, help="file path")

        self.register_forward("data", type=Any, help="json object")

    def perform(self, args):

        data = args.data["_"]

        if args.outfile:

            output_file = open(args.outfile["_"], 'w')
            json.dump(data, output_file, indent=4, separators=(',', ': '))
            output_file.write('\n')

            output_file.close()

        self.add_forward(data=json.dumps(data))
