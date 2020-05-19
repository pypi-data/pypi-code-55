'''
Presets for configuration file
'''

import sys

from ..version import __version__ as version

__all__ = 'DEFAULT', 'OVERWRITE'


DEFAULT = {
    'gui': ('gui-tkinter', str),
    'font_size': ('14', int),
    'icon_size': ('1.0', float),
    'map_size': ('1.0', float),
    'autotracking': (False, bool),
    'usb2snes_device': ('', str),
    'usb2snes_debug': (False, bool),
    'autosave': ('autosave.json', str),
    'button_layout': ('buttons.json', str),
    'window_layout': ('windows.json', str),
    'path_trace': ('', str),
    'usb2snes_server': ('localhost:8080', str),

    'entrance_randomiser': (False, bool),
    'world_state': ('Open', str),
    'glitch_mode': ('None', str),
    'item_placement': ('Advanced', str),
    'dungeon_items': ('Standard', str),
    'goal': ('Defeat Ganon', str),
    'swords': ('Randomised', str),
    'enemiser': (False, bool),
    'shopsanity': (False, bool),

    'majoronly': (False, bool),
}


OVERWRITE = {
    '0.9.0': set(),
    '0.9.1': set(),
    '0.9.2': set(),
    '0.9.3': set(),
    '0.9.4': set(),
    '0.9.5': set(),
    '0.9.6': set(),
    '0.9.7': set(),
    '0.9.8': set(),
    '0.9.9': set(),
    '0.9.10': set(),
    '0.9.11': set(),
}
