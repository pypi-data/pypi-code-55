"""Top-level package for pyh2m."""

__author__ = """goooice"""
__email__ = 'devel0per1991@outlook.com'
__version__ = '0.1.2'

from .h2m import h2m

def feed(html_string):
    h2m.feed(html_string)

def md():
    return h2m.md()