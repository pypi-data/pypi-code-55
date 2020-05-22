import collections
from typing import Dict, Iterable, List, Optional, Tuple

from keydope import mods
from keydope.keycodes import Key


def _is_english_letter(key: Key) -> bool:
    if len(key.name) != 1:
        return False
    return 65 <= ord(key.name) < 91


# pylint: disable=too-many-return-statements
def _get_key_class(key: Key) -> str:
    if _is_english_letter(key):
        return 'letter'
    if 2 <= key.value < 12:
        return 'number'
    if mods.key_to_modifier(key):
        return 'modifier'
    if 59 <= key.value < 69 or key in (Key.F11, Key.F12):
        return 'f_key'
    if 71 <= key.value < 84 or key.name in ('KPASTERISK', 'KPENTER'):
        return 'numpad'
    if key in ('SCROLLLOCK', 'NUMLOCK', 'CAPSLOCK'):
        return 'lock'
    if key.name in ('LEFT', 'RIGHT', 'UP', 'DOWN', 'PAGE_UP', 'PAGE_DOWN',
                    'HOME', 'END'):
        return 'navigation'
    if key.name in ('MINUS', 'EQUAL', 'LEFT_BRACE', 'RIGHT_BRACE', 'SEMICOLON',
                    'APOSTROPHE', 'GRAVE', 'COMMA', 'DOT', 'SLASH'):
        return 'symbol'
    return 'other'


def key_distance(lhs: Key, rhs: Key) -> float:
    if rhs == lhs:
        return 0
    lhs_mod = mods.key_to_modifier(lhs)
    rhs_mod = mods.key_to_modifier(rhs)
    # Different keys but the same modifier.
    if lhs_mod and lhs_mod == rhs_mod:
        return 1
    if _get_key_class(lhs) == _get_key_class(rhs):
        return 2
    # One mod and one regular key.
    if lhs_mod or rhs_mod:
        return 4
    return 3


def map_key_sets(input_keys: Iterable[Key], output_keys: Iterable[Key]):
    input_key_to_output_keys = {}
    for input_key in input_keys:
        input_key_to_output_keys[input_key] = []
    for output_key in output_keys:
        # pylint: disable=cell-var-from-loop
        nearest_input_key = min(
            input_keys, key=lambda k: key_distance(k, output_key))
        input_key_to_output_keys[nearest_input_key].append(output_key)
    return input_key_to_output_keys
