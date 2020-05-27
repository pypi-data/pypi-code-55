'''
TTK style settings
'''

import tkinter.ttk as ttk

from .config import CONFIG, FONT

__all__ = 'init',


def init() -> None:
    '''
    Initialise ttk style.
    '''

    style = ttk.Style()
    style.configure('.', font=FONT)
    for wtype in ('Frame', 'Label'):
        style.configure(f'themed.T{wtype:s}', background=CONFIG['background'],
                        foreground=CONFIG['foreground'])
