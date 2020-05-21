# -*- coding: utf-8 -*-
"""
–––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––
# Identifier
Module | `identifier.py`

Daniel Bakas Amuchastegui\
May 21, 2020

Copyright © Semantyk 2020. All rights reserved.\
–––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––
"""

__all__ = ['Identifier']

from ..node import Node

class Identifier(Node, str):
    pass