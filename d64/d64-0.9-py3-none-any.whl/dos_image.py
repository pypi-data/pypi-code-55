import struct
import mmap

from .block import Block
from .dir_entry import DirEntry
from .dos_path import DOSPath
from .exceptions import DiskFullError


class DOSImage(object):
    def __init__(self, filename):
        self.filename = filename
        self.map = None
        self.fileh = None

    def directory(self, drive=0):
        dos_info = struct.pack('<BB', self.dos_version, self.dos_type[1])
        yield '{} "{:16}" {} {}'.format(drive, self.name.decode(), self.id.decode(), dos_info.decode())
        for path in self.iterdir():
            closed_ch = ' ' if path.entry.closed else '*'
            file_type = path.entry.file_type
            if path.entry.protected:
                file_type += '<'
            yield '{:5}{:18}{}{}'.format(str(path.size_blocks), '"'+str(path)+'"', closed_ch, file_type)
        yield '{} BLOCKS FREE.'.format(self.bam.total_free())

    def open(self, mode):
        self.fileh = open(self.filename, mode)
        self.writeable = mode == 'r+b'
        access = mmap.ACCESS_WRITE if self.writeable else mmap.ACCESS_READ
        self.map = mmap.mmap(self.fileh.fileno(), 0, access=access)
        self.dir_block = Block(self, self.DIR_TRACK, 0)

    def close(self):
        if self.map:
            self.map.close()
        if self.fileh:
            self.fileh.close()

    def iterdir(self, include_deleted=False):
        """Iterate over a directory."""
        block = Block(self, self.DIR_TRACK, 1)

        while block:
            for offset in range(0, Block.SECTOR_SIZE, DirEntry.ENTRY_SIZE):
                entry = DirEntry(block, offset)
                if include_deleted or not entry.is_deleted:
                    yield DOSPath(self, entry=entry)

            block = block.next_block()

    def glob(self, pattern, include_deleted=False):
        """Return paths that match a wildcard pattern."""
        for path in self.iterdir(include_deleted):
            if DOSPath.wildcard_match(path.entry.name, path.entry.file_type, pattern):
                yield path

    def get_free_entry(self):
        """Return an unused entry with first data block for a new path."""
        first_block = self.alloc_first_block()
        if first_block is None:
            return None
        first_block.data_size = 0

        block = Block(self, self.DIR_TRACK, 1)
        entry = None

        # search directory for first free entry
        while block:
            for offset in range(0, Block.SECTOR_SIZE, DirEntry.ENTRY_SIZE):
                e = DirEntry(block, offset)
                if e.is_deleted:
                    entry = e
                    break

            last_block = block
            block = block.next_block()

        if entry is None:
            # no free entry, append a new block to the directory
            block = self.alloc_next_block(last_block.track, last_block.sector, self.DIR_INTERLEAVE)
            if block is None:
                self.free_block(first_block)
                return None

            block.data_size = Block.SECTOR_SIZE-2
            last_block.set_next_block(block)
            entry = DirEntry(block, 0)

        entry.reset(first_block)

        return entry

    def path(self, name):
        if isinstance(name, str):
            name = name.encode()
        paths = [e for e in self.glob(name)]
        if paths:
            # existing path
            return paths[0]
        return DOSPath(self, name=name)

    def free_block(self, block):
        """Mark a block as free in the BAM."""
        self.bam.set_free(block.track, block.sector)

    def block_start(self, track, sector):
        if track == 0 or track > self.MAX_TRACK:
            raise ValueError("Invalid track, %d" % track)

        sector_start = 0
        for sectors, track_range in self.TRACK_SECTOR_MAX:
            if track > track_range[1]:
                sector_start += (track_range[1]-track_range[0]+1) * sectors
            else:
                if sector >= sectors:
                    raise ValueError("Invalid sector, %d:%d" % (track, sector))
                sector_start += (track-track_range[0]) * sectors
                sector_start += sector
                break

        return sector_start*Block.SECTOR_SIZE

    def max_sectors(self, track):
        """Return the maximum sectors for a given track."""
        if track < 1:
            raise ValueError("Invalid track, %d" % track)

        for sectors, track_range in self.TRACK_SECTOR_MAX:
            if track <= track_range[1]:
                return sectors

        raise ValueError("Invalid track, %d" % track)

    def clone_chain(self, block):
        """Return a duplicate of a chain of blocks."""
        new_block = self.alloc_next_block(block.track, block.sector)
        if new_block is None:
            raise DiskFullError

        new_block.set(0, block.get(0, block.SECTOR_SIZE))

        if not block.is_final:
            # recurse for next block
            new_block.set_next_block(self.clone_chain(block.next_block()))

        return new_block

    @property
    def dos_version(self):
        return self.dir_block.get(0xa5)

    @property
    def name(self):
        name = self.dir_block.get(0x90, 0xa0)
        return name.rstrip(b'\xa0')

    @property
    def id(self):
        id = self.dir_block.get(0xa2, 0xa4)
        return id

    @property
    def dos_type(self):
        return self.dir_block.get(2), self.dir_block.get(0xa6)

    @dos_version.setter
    def dos_version(self, version):
        self.dir_block.set(0xa5, version)

    @name.setter
    def name(self, nam):
        self.dir_block.set(0x90, nam.ljust(16, b'\xa0'))

    @id.setter
    def id(self, did):
        if len(did) != 2:
            raise ValueError("Invalid disk id, "+str(did))
        self.dir_block.set(0xa2, did)

    @dos_type.setter
    def dos_type(self, dtype):
        if len(dtype) != 2:
            raise ValueError("Invalid DOS type, "+str(dtype))
        self.dir_block.set(2, dtype[0])
        self.dir_block.set(0xa6, dtype[1])
