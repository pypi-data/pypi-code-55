from typing import Dict, List, Tuple

# TODO(infokiller): Figure out
# pylint: disable=no-name-in-module
from keydope import keycodes, mods
from keydope.mods import Modifier

COMBO_SEPARATOR = '-'

_MODIFIER_TO_STRINGS = {
    Modifier.CONTROL: ['Ctrl', 'C'],
    Modifier.ALT: ['Alt', 'M'],
    Modifier.SHIFT: ['Shift'],
    Modifier.SUPER: ['Super'],
    Modifier.ISO_LEVEL3: ['LV3'],
    Modifier.ISO_LEVEL5: ['LV5'],
}


def _invert_dict_to_list(input_dict: dict) -> dict:
    inverted = {}
    for key, values in input_dict.items():
        for value in values:
            inverted[value] = key
    return inverted


_STRING_TO_MODIFIER = _invert_dict_to_list(_MODIFIER_TO_STRINGS)


def parse_key_name(key_name: str) -> List[keycodes.Key]:
    if key_name in _STRING_TO_MODIFIER:
        modifier = _STRING_TO_MODIFIER[key_name]
        modifier_keys = mods.modifier_to_keys(modifier)
        if not modifier_keys:
            raise ValueError(
                'No modifier key is assigned to modifier: {}'.format(
                    modifier.name))
        return modifier_keys
    if not hasattr(keycodes.Key, key_name.upper()):
        raise ValueError('Unknown key: {}'.format(key_name))
    return [getattr(keycodes.Key, key_name.upper())]


def _get_key_to_sort_key() -> Dict[keycodes.Key, int]:
    # Start by setting the values for all keys, ignoring if they are modifiers
    # or not. We later override the values for modifiers. This ensures that if
    # a new modifier is added, it will have the correct value. Otherwise, if we
    # started by setting the values for modifer keys, the code setting the
    # values for regular keys would override it.
    # If a modifier is removed, this function will fail to run (for example
    # because `Modifier.Control` will no longer be defined).
    Key = keycodes.Key
    key_to_sort_key = {}
    ordered_keys = [
        Key.LEFT_CTRL, Key.RIGHT_CTRL, Key.LEFT_ALT, Key.RIGHT_ALT,
        Key.LEFT_META, Key.RIGHT_META, Key.LEFT_SHIFT, Key.RIGHT_SHIFT,
        Key.SPACE, Key.ENTER, Key.BACKSPACE, Key.DELETE, Key.TAB, Key.CAPSLOCK,
        Key.A, Key.B, Key.C, Key.D, Key.E, Key.F, Key.G, Key.H, Key.I, Key.J,
        Key.K, Key.L, Key.M, Key.N, Key.O, Key.P, Key.Q, Key.R, Key.S, Key.T,
        Key.U, Key.V, Key.W, Key.X, Key.Y, Key.Z
    ]
    for i, key in enumerate(ordered_keys):
        # 0-9 are reserved for modifiers, so we start with 10.
        key_to_sort_key[key] = 10 + i
    last_sort_key = max(key_to_sort_key.values())
    for key in set(Key) - set(ordered_keys):
        key_to_sort_key[key] = last_sort_key + 1
        last_sort_key += 1
    mod_to_sort_key = {
        Modifier.CONTROL: 0,
        Modifier.ISO_LEVEL3: 1,
        Modifier.ISO_LEVEL5: 2,
        Modifier.ALT: 3,
        Modifier.SUPER: 4,
        Modifier.SHIFT: 5,
    }
    for mod in Modifier:
        for key in mods.modifier_to_keys(mod):
            key_to_sort_key[key] = mod_to_sort_key.get(mod, 9)
    return key_to_sort_key


_KEY_TO_SORT_KEY = _get_key_to_sort_key()


def combo_to_str(combo: mods.Combo) -> str:
    mod_keys = combo.get_mod_keys()
    regular_keys = list(combo.keys - set(mod_keys))
    return COMBO_SEPARATOR.join(k.name for k in sorted(
        mod_keys + regular_keys, key=lambda k: _KEY_TO_SORT_KEY.get(k, 1000)))


def parse_combo(combo_str: str) -> mods.Combo:
    combo_keys = set()
    for key_name in combo_str.split(COMBO_SEPARATOR):
        keys = parse_key_name(key_name)
        combo_keys.add(next(iter(keys)))
    return mods.Combo(combo_keys)


class ComboSpec:

    def __init__(self, key_sets: List[List[keycodes.Key]], exact_match=True):
        key_tuples = []
        for keys in key_sets:
            key_tuples.append(tuple(keys))
        self.key_sets = tuple(key_tuples)
        self.exact_match: bool = exact_match

    def match(self, combo):
        # Every list in key_sets must have at least one key satisfied by the
        # combo.
        matched_combo_keys = set()
        for keys in self.key_sets:
            matched_key = None
            for k in combo.keys:
                if k in keys:
                    matched_key = k
                    break
            if not matched_key:
                return False
            matched_combo_keys.add(matched_key)
        if self.exact_match and matched_combo_keys != combo.keys:
            return False
        return True

    def __eq__(self, other):
        if isinstance(other, ComboSpec):
            return self.__dict__ == other.__dict__
        return NotImplemented

    def __hash__(self):
        return hash(frozenset((self.key_sets, self.exact_match)))


def parse_combo_spec(keyspec_str: str, exact_match: bool = True) -> ComboSpec:
    key_sets = []
    for key_name in keyspec_str.split(COMBO_SEPARATOR):
        key_sets.append(parse_key_name(key_name))
    return ComboSpec(key_sets, exact_match)
