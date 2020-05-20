import struct

from .block import Block


class DirEntry(object):
    ENTRY_SIZE = 0x20
    FTYPE_STR = ('DEL', 'SEQ', 'PRG', 'USR', 'REL', '???', '???', '???')

    def __init__(self, block, entry_offset):
        self.block = block
        self.entry_offset = entry_offset

    def _file_type(self):
        return self.block.get(self.entry_offset+2)

    def first_block(self):
        """Return the first block containing file data."""
        return Block(self.block.image, *self.start_ts)

    def reset(self, first_block):
        """Reset an entry for reuse."""
        self.file_type = 0
        self.size = 1
        self.start_ts = (first_block.track, first_block.sector)

    @property
    def is_deleted(self):
        """Return `True` if this entry is no longer in use."""
        return self._file_type() == 0

    @property
    def file_type(self):
        return self.FTYPE_STR[self._file_type() & 7]

    @property
    def protected(self):
        return bool(self._file_type() & 0x40)

    @property
    def closed(self):
        return bool(self._file_type() & 0x80)

    @property
    def start_ts(self):
        return struct.unpack('<BB', self.block.get(self.entry_offset+3, self.entry_offset+5))

    @property
    def name(self):
        name = self.block.get(self.entry_offset+5, self.entry_offset+0x15)
        return name.rstrip(b'\xa0')

    @property
    def side_sector_ts(self):
        """Return track and sector of first side sector."""
        return struct.unpack('<BB', self.block.get(self.entry_offset+0x15, self.entry_offset+0x17))

    @property
    def record_len(self):
        """Return relative file record length."""
        return self.block.get(self.entry_offset+0x17)

    @property
    def size(self):
        size, = struct.unpack('<H', self.block.get(self.entry_offset+0x1e, self.entry_offset+0x20))
        return size

    @file_type.setter
    def file_type(self, ftype):
        if isinstance(ftype, str):
            if ftype.upper() not in self.FTYPE_STR:
                raise ValueError("Unknown file type, "+ftype)
            ftype = self.FTYPE_STR.index(ftype.upper()) | 0x80

        self.block.set(self.entry_offset+2, ftype)

    @protected.setter
    def protected(self, prot):
        val = 0x40 if prot else 0
        old = self._file_type()
        self.block.set(self.entry_offset+2, old & 0xbf | val)

    @closed.setter
    def closed(self, clsd):
        val = 0x80 if clsd else 0
        old = self._file_type()
        self.block.set(self.entry_offset+2, old & 0x7f | val)

    @start_ts.setter
    def start_ts(self, ts):
        self.block.set(self.entry_offset+3, struct.pack('<BB', *ts))

    @name.setter
    def name(self, name):
        self.block.set(self.entry_offset+5, name[:16].ljust(16, b'\xa0'))

    @side_sector_ts.setter
    def side_sector_ts(self, ts):
        """Modify track and sector of first side sector."""
        self.block.set(self.entry_offset+0x15, struct.pack('<BB', *ts))

    @record_len.setter
    def record_len(self, rec_len):
        """Modify relative file record length."""
        self.block.set(self.entry_offset+0x17, rec_len)

    @size.setter
    def size(self, size):
        self.block.set(self.entry_offset+0x1e, struct.pack('<H', size))
