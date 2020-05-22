"""Top-level package for pyh2m."""

__author__ = """goooice"""
__email__ = 'devel0per1991@outlook.com'
__version__ = '0.2.0'

from .h2m import h2m, HTMLParserToMarkDown
def set_debug_level(level):
    h2m.set_debug_level(level)
    
def feed(html_string):
    h2m.feed(html_string)

def md():
    return h2m.md()

def new_h2m():
    return HTMLParserToMarkDown()