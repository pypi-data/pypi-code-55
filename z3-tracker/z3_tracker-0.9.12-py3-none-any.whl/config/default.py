'''
Presets for configuration file
'''

import sys

from ..version import __version__ as version

__all__ = 'DEFAULT', 'CONFLICTS', 'OVERWRITE'


DEFAULT = {
    'gui': ('gui-tkinter', str),
    'font_size': ('14', int),
    'icon_size': ('1.0', float),
    'map_size': ('1.0', float),
    'usb2snes_debug': (False, bool),
    'foreground': ('#000000', str),
    'background': ('#d9d9d9', str),
    'autotracking': (False, bool),
    'usb2snes_device': ('', str),
    'autodefault_items': (True, bool),
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
    'shuffle_map': (False, bool),
    'shuffle_compass': (False, bool),
    'shuffle_smallkey': (False, bool),
    'shuffle_bigkey': (False, bool),
    'goal': ('Defeat Ganon', str),
    'swords': ('Randomised', str),
    'enemiser': (False, bool),
    'shopsanity': (False, bool),

    'majoronly': (False, bool),
}


CONFLICTS = (
    {'entrance_randomiser': (True, 'Entrance Randomiser'),
     'majoronly': (True, 'Major Locations Only')},
)


OVERWRITE = {
    '0.9.0': set(), '0.9.1': set(), '0.9.2': set(), '0.9.3': set(),
    '0.9.4': set(), '0.9.5': set(), '0.9.6': set(), '0.9.7': set(),
    '0.9.8': set(), '0.9.9': set(),
    '0.9.10': set(),
    '0.9.11': set(),
    '0.9.12': set(),
}
