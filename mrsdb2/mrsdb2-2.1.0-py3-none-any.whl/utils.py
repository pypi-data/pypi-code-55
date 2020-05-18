import pickle
import binascii


def Pickle(obj, *args, **kwargs):
    """
    Make a (pickleable) Python object database writable.
    """
    p = binascii.hexlify(pickle.dumps(obj, *args, **kwargs)).decode("utf-8")
    return f'$PYCKLE:{p}'


def BigInt(i):
    """
    Make an integer over 64 bits database writable.
    """
    if i.bit_length() >= 64:
        return f'$BIGINT:{i}'
    else:
        return i


def BigFloat(i):
    """
    Make a float over 64 bits database writable.
    """
    if i.bit_length() >= 64:
        return f'$BIGFLT:{i}'
    else:
        return i