import pickle
import binascii


def Pickle(obj, legacy=False, *args, **kwargs):
    """
    Make a (pickleable) Python object database writable.
    """
    p = binascii.hexlify(pickle.dumps(obj, *args, **kwargs)).decode("utf-8")
    if legacy:
        return f'$PYCKLE:{p}'
    else:
        return ('$PYCKLE', p)


def BigInt(i, legacy=False):
    """
    Make an integer over 64 bits database writable.
    """
    if i.bit_length() >= 64:
        if legacy:
            return f'$BIGINT:{i}'
        else:
            return ('BIGINT', str(i))
    else:
        return i


def BigFloat(i, legacy=False):
    """
    Make a float over 64 bits database writable.
    """
    if i.bit_length() >= 64:
        if legacy:
            return f'$BIGFLT:{i}'
        else:
            return ('BIGFLT', str(i))
    else:
        return i