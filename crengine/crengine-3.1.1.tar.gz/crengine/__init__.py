######################################################################
### Change Ringing Engine
### Copyright (c) 2020 Jonathan Wilson
### Please refer to help/licence.txt for further information
### File: __init__.py
### Description: Enable crengine to be imported
### Last Modified: 24 May 2020
######################################################################

'''\
Change Ringing Engine is a method ringing application for church bell
ringers. It works out all the rows of a method (plain course or touch,
displays them in a variety of formats and even rings them audibly on a
set of bell sample sound files. Change Ringing Engine uses a
traditional command line interface, but may be embedded as an API in
another application such as Bell View.'''

from .engine import Engine, CREError

