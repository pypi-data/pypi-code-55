'''
Autotracker GUI interaction
'''


import logging as log
import tkinter as tk
import tkinter.ttk as ttk

from ..config import CONFIG

FOREGROUND = CONFIG['foreground']
FRAME = None
INFOSTRING = None
INFOTEXT = None
REFRESH = None

__all__ = (
    'FRAME', 'INFOSTRING', 'INFOTEXT', 'REFRESH', 'set_info', 'AutotrackToggle')


def set_info(message: str, msgtype: str = None, tolog: bool = True,
             refreshbutton: bool = True) -> None:
    '''
    Set autotracker status message.

    Args:
        message: status message
        msgtype: 'info' or 'error' or None
        tolog: if False, message won't be copied to stdout
        refreshbutton: True if refreshbutton should be shown
    '''

    assert msgtype in ('info', 'error', None)
    if not message:
        if tolog:
            log.debug('Resetting info.')
        INFOSTRING.set('')
        FRAME.grid_remove()
    else:
        if refreshbutton:
            FRAME.refreshbutton.grid()
        else:
            FRAME.refreshbutton.grid_remove()
        if msgtype is not None:
            if tolog:
                if msgtype == 'error':
                    log.warning('%s', message)
                else:
                    log.info('%s', message)
        INFOSTRING.set('{0:s}{1:s}'.format(
            'ERROR:\n' if msgtype == 'error' else '', message))
        if msgtype == 'error':
            INFOTEXT.configure(foreground='#bb0000')
        elif msgtype is not None:
            INFOTEXT.configure(foreground='#000000')
        FRAME.grid()


class AutotrackToggle(ttk.Label):
    '''
    Switch allowing autotracker for specific display to be switched off.

    Instance variables:
        attext: button label
        toggle: True if autotracking is on
    '''

    def __init__(self, *args, **kwargs):
        '''
        Args:
            default: default state; True means autotracking enabled
            args, kwargs: arguments of ttk.Label()
        '''

        self.toggle = kwargs['default']
        self.attext = tk.StringVar()
        del kwargs['default']
        kwargs.update({'borderwidth': 1, 'textvariable': self.attext})
        super().__init__(*args, **kwargs)
        self.defaultcolour = CONFIG['background']
        self.bind('<ButtonRelease-1>',
                  lambda _: self.set_autotracking(not self.toggle))
        self.disable()

    def disable(self) -> None:
        '''
        Disable button.
        '''

        self.attext.set('')
        self.configure(background=self.defaultcolour, relief=tk.FLAT)

    def enable(self) -> None:
        '''
        Enable button.
        '''

        self.configure(relief=tk.GROOVE)
        self.set_autotracking(self.toggle)

    def set_autotracking(self, autotrack: bool) -> None:
        '''
        Set autotracker.

        Args:
            autotrack: True if autotracker should be switched on
        '''

        self.toggle = autotrack
        if autotrack:
            self.attext.set(' Auto ')
        else:
            self.attext.set(' Manual ')
            self.configure(
                background=self.defaultcolour, foreground=FOREGROUND)

    def set_state(self, state: str) -> None:
        '''
        Set autotracking status.

        Args:
            state: 'on', 'off' or 'error'
        '''

        if not self.toggle:
            return
        assert state in ('on', 'off', 'error')
        colour = (
            '#bb0000' if state == 'error' else
            '#bb6b00' if state == 'off' else
            '#0000bb')
        self.configure(background=colour, foreground='white')
