"""
Endpoints related to quotes. They all return either one Quote object or a sequence of it.

A Quote is a named tuple with ``id`` and ``text`` fields.

https://xtools.readthedocs.io/en/stable/api/quote.html
"""

from typing import Sequence
from collections import namedtuple

from . import base

Quote = namedtuple("Quote", ("id", "text"), module=__name__)


def _get_quotes(path: str) -> Sequence[Quote]:
    raw_quotes = base.get(path)
    quotes = []

    for quote_id, quote_text in sorted(raw_quotes.items()):
        quotes.append(Quote(int(quote_id), quote_text))

    return quotes


def random_quote() -> Quote:
    """
    Return a random quote.

    https://xtools.readthedocs.io/en/stable/api/quote.html#random-quote

    :return: Quote.
    """
    return _get_quotes("/quote/random")[0]


def single_quote(quote_id: int) -> Quote:
    """
    Get a quote by ID.

    https://xtools.readthedocs.io/en/stable/api/quote.html#single-quote

    :param quote_id:
    :return: Quote.
    """
    return _get_quotes("/quote/%d" % quote_id)[0]


def all_quotes() -> Sequence[Quote]:
    """
    Get all quotes.

    https://xtools.readthedocs.io/en/stable/api/quote.html#all-quotes

    :return: sequence of Quote objects.
    """
    return _get_quotes("/quote/all")