import struct

from .basic_file import BASICFile
from .binary_file import BinaryFile
from .disk_image import DiskImage  # noqa: F401
from .dos_path import DOSPath  # noqa: F401
from .exceptions import ConsistencyError, DiskFullError  # noqa: F401


def ProgramFile(fileh):
    start_addr, = struct.unpack('<H', fileh.read(2))

    if start_addr & 0xFF == 1:
        # BASIC
        return BASICFile(fileh, start_addr)

    return BinaryFile(fileh, start_addr)
