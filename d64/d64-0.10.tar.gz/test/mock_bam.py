from d64.bam import D64BAM
from d64.disk_image import D64Image


class MockD64BAM(object):
    def __init__(self):
        self.entries = [None]
        self.max_sectors = [None]
        self.allocated = set()
        for sectors, range_ in D64Image.TRACK_SECTOR_MAX:
            for t in range(range_[0], range_[1]+1):
                bits_free = '1' * sectors
                self.entries.append((sectors, bits_free))
                self.max_sectors.append(sectors)

    def fill_entry(self, track):
        _, free_bits = self.entries[track]
        self.entries[track] = (self.max_sectors[track], free_bits.replace('0', '1'))

    def clear_entry(self, track):
        _, free_bits = self.entries[track]
        self.entries[track] = (0, free_bits.replace('1', '0'))

    def get_entry(self, track):
        return self.entries[track]

    def set_allocated(self, track, sector):
        total, free_bits = self.entries[track]
        total -= 1
        bits = [b for b in free_bits]
        bits[sector] = '0'
        self.entries[track] = (total, ''.join(bits))

    free_from = D64BAM.__dict__['free_from']
