'''
Item memory locations

Format:
    A dictionary value can be either:
        - int: the address is simply checked for != 0
        - dict: no address is checked, other checks are applied as shown below
        - tuple: must consist of an int and dict; both of above's checks are
            applied
    The dictionary can contain the following keywords:
        - 'flag': an address is checked for a bit-flag; value is (address, flag)
        - 'is': address value needs to equal dict value
        - 'min': address value needs to be higher or equal than dict value
        - 'choice': any condition in the following sequence must be true;
            conditions follow the same rules as a value of the main dictionary
        - 'step': value is {stepping: int or dict or tuple}, a stepping conforms
            to the amount of times an item has been clicked on the display; each
            value in this dictionary follows the same rules as a value of the
            main dictionary
    All keywords are grouped together as AND.
'''


__all__ = 'ITEMS',


ITEMS = {
    'bow': (0x340, {'step': {
        1: None,
        2: (0x340, {'is': 4})
    }}),
    'boomerang': (0x341, {'step': {
        1: {'flag': (0x38c, 0x80)},
        2: {'flag': (0x38c, 0x40)},
        3: {'flag': (0x38c, 0xc0)}
        }}),
    'hookshot': 0x342,
    'bombs': 0x343,
    'mushroompowder': (0x344, {'step': {
        1: {'flag': (0x38c, 0x28)},
        2: {'flag': (0x38c, 0x10)},
        3: {'flag': (0x38c, 0x38)}
        }}),
    'firerod': 0x345,
    'icerod': 0x346,
    'bombos': 0x347,
    'ether': 0x348,
    'quake': 0x349,
    'lantern': 0x34a,
    'hammer': 0x34b,
    'shovelocarina': (0x34c, {'step': {
        1: {'flag': (0x38c, 0x04)},
        2: {'choice': ({'flag': (0x38c, 0x01)}, {'flag': (0x38c, 0x02)})},
        3: {'flag': (0x38c, 0x04), 'choice': (
            {'flag': (0x38c, 0x01)}, {'flag': (0x38c, 0x02)})
        }
    }}),
    'bugnet': 0x34d,
    'mudora': 0x34e,
    'bottle': 0x34f,
    'somaria': 0x350,
    'byrna': 0x351,
    'cape': 0x352,
    'mirror': 0x353,
    'sword': (0x359, {'step': {
        1: None,
        2: (0x359, {'is': 0x02}),
        3: (0x359, {'is': 0x03}),
        4: (0x359, {'is': 0x04})
    }}),
    'shield': (0x35a, {'step': {
        1: None,
        2: (0x35a, {'is': 0x02}),
        3: (0x35a, {'is': 0x03})
    }}),
    'armour': {'step': {
        1: (0x35b, {'is': 0x00}),
        2: (0x35b, {'is': 0x01}),
        3: (0x35b, {'is': 0x02})
    }},
    'pegasus': 0x355,
    'glove': (0x354, {'step': {
        1: None,
        2: (0x354, {'is': 0x02})
    }}),
    'flippers': 0x356,
    'pearl': 0x357,
    'halfmagic': 0x37b,
}
