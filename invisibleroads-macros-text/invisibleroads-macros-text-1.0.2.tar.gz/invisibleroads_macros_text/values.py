import sys


CHARACTER_ENCODING = sys.getfilesystemencoding()


def unicode_safely(x):
    # http://stackoverflow.com/a/23085282/192092
    try:
        return x.decode(CHARACTER_ENCODING)
    except (AttributeError, UnicodeEncodeError):
        return x
