import logging
from os import path
from hashlib import sha512
from binascii import unhexlify, hexlify

logger = logging.getLogger('multiplexer')

THRESHOLD_SIZE = 1000000
SUBKEY_SIZE = 128


def _get_indices(init):
    key = 0
    spacer = 0
    id_spacer = -1
    while spacer < 2 or id_spacer == spacer or key == 0:
        id_spacer += 1
        spacer = int(init[id_spacer], 16)
        key = int(init[spacer], 16)
    return spacer, key


def _step(key):
    init = sha512(key.encode()).hexdigest()

    spacer, key = _get_indices(init)

    phrase = init[::key]

    out = ''
    while phrase:
        out += sha512(phrase[:spacer].encode()).hexdigest()
        phrase = phrase[spacer:]

    return out


def generate(key, save=False, path='book.key'):
    i = 0
    output = ''
    initkey = key
    while len(output) < THRESHOLD_SIZE:
        i += 1
        output += _step(key)
        key = output[:-SUBKEY_SIZE]

    logger.info(f'{i} steps performed')

    if save:
        with open(path, 'wb+') as fp:
            fp.write(unhexlify(output))

    return output


def load(file='book.key'):
    if not path.exists(file) or not path.isfile(file):
        return None
    with open(file, 'rb') as fp:
        return hexlify(fp.read()).decode()
