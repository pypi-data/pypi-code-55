'''
Autotracker
'''


import importlib
import logging as log
import threading
import tkinter
import tkinter.ttk

from ..config import CONFIG

log.basicConfig(level=log.DEBUG if CONFIG['usb2snes_debug'] else log.INFO)

from . import gui
from .gui import set_info, AutotrackToggle

__all__ = ['set_info', 'AutotrackToggle']

try:
    websockets = importlib.import_module('websockets')
except ImportError:
    WEBSOCKETS_AVAILABLE = False
else:
    WEBSOCKETS_AVAILABLE = True

if not WEBSOCKETS_AVAILABLE:
    CONNECTED = threading.Event()
    DEVICES = {''}
    INTERFACES = {}
    STOP = threading.Event()
    def thread(*args, **kwargs):
        interval = 0
        while not STOP.wait(timeout=interval):
            interval = 1
            if CONFIG['autotracking']:
                set_info(
                    'To use autotracking, please install Python websockets.',
                    'error', tolog=False)
            else:
                set_info('', tolog=False)
else:
    log.debug('Found websocket module.')
    from .autotracker import DATA, INTERFACES, STOP, thread
    from .usb2snes import CONNECTED, DEVICES
    __all__.extend(('DATA', 'thread'))

__all__.extend(('CONNECTED', 'DEVICES', 'INTERFACES', 'STOP', 'register_gui'))


def register_gui(infostring: tkinter.StringVar, atframe: tkinter.ttk.LabelFrame,
                 infotext: tkinter.ttk.Label, refresh=threading.Event) -> None:
    '''
    Register autotracker GUI handle.

    Args:
        infostring: display text string
        atframe: main autotracker widget
        infotext: display text object
        refresh: refresh button press event
    '''

    gui.INFOSTRING = infostring
    gui.FRAME = atframe
    gui.INFOTEXT = infotext
    gui.REFRESH = refresh
