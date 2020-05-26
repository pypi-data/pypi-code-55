######################################################################
### Bell View
### Copyright (c) 2020 Jonathan Wilson
### Please refer to help/licence.txt for further information
### File: __main__.py
### Description: Bell View GUI
### Last Modified: 24 May 2020
######################################################################

from sys import argv, exit
from .bvapp import BellViewApp

r=BellViewApp().run_app(argv[1:])
exit(r)




