import enum
from typing import Iterable, Optional, Set

from .keycodes import Key


@enum.unique
class Modifier(enum.Enum):
    '''Real keyboard modifier.'''

    CONTROL, ALT, SHIFT, SUPER, ISO_LEVEL3, ISO_LEVEL5 = range(6)


_MODIFIER_TO_KEYS = {
    Modifier.CONTROL: [Key.LEFT_CTRL, Key.RIGHT_CTRL],
    Modifier.ALT: [Key.LEFT_ALT, Key.RIGHT_ALT],
    Modifier.SHIFT: [Key.LEFT_SHIFT, Key.RIGHT_SHIFT],
    Modifier.SUPER: [Key.LEFT_META, Key.RIGHT_META],
    Modifier.ISO_LEVEL3: [],
    Modifier.ISO_LEVEL5: [Key.CAPSLOCK],
}


def key_to_modifier(key: Key) -> Optional[Modifier]:
    '''Converts a key enum to a modifier enum.'''
    for mod, keys in _MODIFIER_TO_KEYS.items():
        if key in keys:
            return mod
    return None
    # raise ValueError(
    #     'Key {} is not assigned to a modifier. Modifer to keys mapping: {}'.
    #     format(key, _MODIFIER_TO_KEYS))


def modifier_to_keys(modifier: Modifier):
    return _MODIFIER_TO_KEYS[modifier]


def get_all_modifier_keys() -> Set[Key]:
    '''Returns all keys mapped to mods.'''
    all_mods = set()
    for keys in _MODIFIER_TO_KEYS.values():
        all_mods.update(keys)
    return all_mods


class Combo:

    def __init__(self, keys: Iterable[Key]):
        self.keys = set(keys)

    def get_mod_keys(self):
        modifier_keys = []
        for key in self.keys:
            modifier = key_to_modifier(key)
            if modifier:
                modifier_keys.append(key)
        return modifier_keys

    def get_mods(self):
        return set(key_to_modifier(key) for key in self.get_mod_keys())

    def __eq__(self, other):
        if isinstance(other, Combo):
            return self.keys == other.keys
        return NotImplemented

    def __hash__(self):
        return hash(frozenset(self.keys))
