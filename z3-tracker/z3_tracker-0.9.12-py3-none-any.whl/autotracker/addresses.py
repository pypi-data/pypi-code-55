'''
General purpose memory address list.
'''


WRAM = 0xf50000
SAVE = WRAM + 0xf000

GAMEMODE = WRAM + 0x10, 1
ITEMS = SAVE + 0x340, 79


__all__ = 'GAMEMODE', 'ITEMS'
