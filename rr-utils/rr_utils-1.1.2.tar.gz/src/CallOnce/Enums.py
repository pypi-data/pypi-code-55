from enum import IntEnum


class ArgumentsMode(IntEnum):
    IGNORE = 1
    SERIALIZE_AND_HASH = 2


class HashFunction(IntEnum):
    PYTHON = 1
    MD5 = 2


class StorageMode(IntEnum):
    Memory = 1
    Disk = 2
