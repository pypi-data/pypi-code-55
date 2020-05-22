"""Bencode decoder implementation.

This module is implemented for decoding seyhuns_bencode string from an URL.

Usage:
  seyhuns_bencode decode URL
"""
import logging

from docopt import docopt

from seyhuns_bencode import __version__
from seyhuns_bencode.bencode import BencodeParser
from seyhuns_bencode.exceptions import InputError


__all__ = ('main',)


logger = logging.getLogger(__name__)


def main():
    arguments = docopt(__doc__, version=__version__)
    if arguments.get('decode'):
        try:
            decoder = BencodeParser(arguments.get('URL'))
        except InputError as e:
            logger.exception(exc_info=e)
            exit(1)
        else:
            print(decoder())


if __name__ == '__main__':
    main()
