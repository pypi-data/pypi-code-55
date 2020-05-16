# -*- coding: utf-8 -*-

from enum import Enum


class EntityStatus(Enum):
    created = 1
    filled = 2
    modified = 3
    addedobject = 4
    deleted = 5
