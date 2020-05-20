import struct

from .exceptions import ConsistencyError


class D64BAM(object):

    BAM_OFFSET = 4
    BAM_ENTRY_SIZE = 4

    def __init__(self, image):
        self.image = image

    def get_entry(self, track):
        """Return a tuple of total free blocks and a string of free blocks for a track."""
        if track == 0 or track > self.image.MAX_TRACK:
            raise ValueError("Invalid track, %d" % track)

        start = self.BAM_OFFSET+(track-1)*self.BAM_ENTRY_SIZE
        packf = "<{}B".format(self.BAM_ENTRY_SIZE)
        e = struct.unpack(packf, self.image.dir_block.get(start, start+self.BAM_ENTRY_SIZE))
        free_bits = ''
        for b in e[1:]:
            free_bits += ''.join(reversed(format(b, '08b')))

        return e[0], free_bits

    def set_entry(self, track, total, free_bits):
        """Update the block allocation entry for a track."""
        if track == 0 or track > self.image.MAX_TRACK:
            raise ValueError("Invalid track, %d" % track)

        start = self.BAM_OFFSET+(track-1)*self.BAM_ENTRY_SIZE
        packf = "<{}B".format(self.BAM_ENTRY_SIZE)
        entry = [total]
        while free_bits:
            val = ''.join(reversed(free_bits[:8]))
            entry.append(int(val, 2))
            free_bits = free_bits[8:]
        bin_entry = struct.pack(packf, *entry)
        self.image.dir_block.set(start, bin_entry)

    def is_allocated(self, track, sector):
        """Return `True` if a block is in use."""
        _, free_bits = self.get_entry(track)
        if sector >= len(free_bits):
            raise ValueError("Invalid sector, %d:%d" % (track, sector))
        return free_bits[sector] == '0'

    def set_allocated(self, track, sector):
        """Set a block as in use."""
        total, free_bits = self.get_entry(track)
        if sector >= len(free_bits):
            raise ValueError("Invalid sector, %d:%d" % (track, sector))
        if free_bits[sector] == '0':
            raise ValueError("Sector already allocated, %d:%d" % (track, sector))
        if total == 0:
            raise ConsistencyError("BAM mismatch track %d, free count %d, bits %s" % (track, total, free_bits))
        bits = [b for b in free_bits]
        bits[sector] = '0'
        total -= 1
        self.set_entry(track, total, ''.join(bits))

    def set_free(self, track, sector):
        """Set a block as not in use."""
        total, free_bits = self.get_entry(track)
        if sector >= len(free_bits):
            raise ValueError("Invalid sector, %d:%d" % (track, sector))
        if free_bits[sector] == '1':
            raise ValueError("Sector already free, %d:%d" % (track, sector))
        bits = [b for b in free_bits]
        bits[sector] = '1'
        total += 1
        self.set_entry(track, total, ''.join(bits))

    def entries(self, include_dir_track=False):
        """Iterator returning each track entry."""
        for track in range(1, self.image.MAX_TRACK+1):
            if track != self.image.DIR_TRACK or include_dir_track:
                yield self.get_entry(track)

    def total_free(self):
        """Return total free blocks."""
        return sum([e[0] for e in self.entries()])

    def check(self):
        """Perform a consistency check of the BAM."""
        for track in range(1, self.image.MAX_TRACK+1):
            total, free_bits = self.get_entry(track)
            if total != free_bits.count('1'):
                raise ConsistencyError("BAM mismatch track %d, free count %d, bits %s" % (track, total, free_bits))

    @staticmethod
    def free_from(free_bits, start):
        """Return the first free sector starting at `start`, wrapping if necessary."""
        if '1' not in free_bits:
            raise ConsistencyError("BAM inconsistent")

        # double up the bits so wrapping occurs
        wrap_bits = free_bits * 2
        i = wrap_bits.find('1', start)
        if i > len(free_bits):
            # wrapped back to start, adjust
            i -= len(free_bits)
        return i
