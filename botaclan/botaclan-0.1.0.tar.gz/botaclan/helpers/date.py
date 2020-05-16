from collections import namedtuple


def create_tuple_from_dateparser_found(found: tuple) -> namedtuple:
    return namedtuple("custom_date", ["content", "datetime"])(*found)
