# -*- coding: utf-8 -*-
""" gateway error classes.

"""

__all__ = ["TokenInvalid", "InvalidItemType", "ItemDoesNotExist", "ItemExists"]


class TokenInvalid(Exception):
    pass


class InvalidItemType(TypeError):
    pass


class ItemExists(Exception):
    pass


class ItemDoesNotExist(Exception):
    pass
