#!/usr/bin/env python
 
"""
pyplayground.py
 
Platform for simple games
 
URL:     https://github.com
Author:  Mychajlo Chodorev
License: Do What The Fuck You Want To Public License (WTFPL)
         See http://www.wtfpl.net/
"""

import pygame
from inspect import isclass
from pkgutil import iter_modules
from pathlib import Path
from importlib import import_module

package_dir = Path(__file__).resolve().parent
for (_, module_name, _) in iter_modules([package_dir]):

    # import the module and iterate through its attributes
    module = import_module(f"{__name__}.{module_name}")
    for attribute_name in dir(module):
        attribute = getattr(module, attribute_name)

        if isclass(attribute):            
            # Add the class to this package's variables
            globals()[attribute_name] = attribute

for attribute_name in dir(pygame):
    globals()[attribute_name] = getattr(pygame, attribute_name)
        
if __name__ == "__main__":
    pygame.init()