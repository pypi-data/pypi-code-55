######################################################################
### Change Ringing Engine
### Copyright (c) 2020 Jonathan Wilson
### Please refer to help/licence.txt for further information
### File: __main__.py
### Description: Run Change Ringing Engine command line tool
### Last Modified: 24 May 2020
######################################################################

### import modules

from sys import argv, exit
from .engine import Engine

### uncomment the following lines to allow line editing

#import readline
#import rlcompleter

#if 'libedit' in readline.__doc__:
#    readline.parse_and_bind("bind ^I rl_complete")
#else:
#    readline.parse_and_bind("tab: complete")


### create an instance of the ringing engine

r=Engine().runengine(argv[1:])
exit(r)

