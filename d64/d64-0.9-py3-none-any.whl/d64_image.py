from .bam import D64BAM
from .block import Block
from .dos_image import DOSImage


class D64Image(DOSImage):

    MAX_TRACK = 35
    DIR_TRACK = 18
    INTERLEAVE = 10
    DIR_INTERLEAVE = 3
    TRACK_SECTOR_MAX = ((21, (1, 17)), (19, (18, 24)), (18, (25, 30)), (17, (31, 35)))

    def __init__(self, filename):
        self.bam = D64BAM(self)
        super().__init__(filename)

    def alloc_first_block(self):
        """Allocate the first block for a new file."""
        track = None
        for low, high in zip(range(self.DIR_TRACK-1, 0, -1), range(self.DIR_TRACK+1, self.MAX_TRACK+1)):
            total, free_bits = self.bam.get_entry(low)
            if total:
                track = low
                break
            total, free_bits = self.bam.get_entry(high)
            if total:
                track = high
                break

        if track is None:
            # tried either side of the directory, disk is full
            return None
        sector = self.bam.free_from(free_bits, 0)

        self.bam.set_allocated(track, sector)
        return Block(self, track, sector)

    def alloc_next_block(self, track, sector, interleave=INTERLEAVE):
        """Allocate a subsequent block for a file."""
        cur_track = track
        cur_sector = sector
        delta = -1 if track < self.DIR_TRACK else 1
        tries = 2  # either side of directory track

        while True:
            total, free_bits = self.bam.get_entry(cur_track)
            if total:
                # free sector in current track
                cur_sector += interleave
                if cur_sector >= self.max_sectors(cur_track):
                    cur_sector -= self.max_sectors(cur_track)
                    if cur_sector:
                        cur_sector -= 1

                cur_sector = self.bam.free_from(free_bits, cur_sector)
                self.bam.set_allocated(cur_track, cur_sector)
                return Block(self, cur_track, cur_sector)

            if cur_track == self.DIR_TRACK:
                # tried either side of the directory then the directory, disk is full
                return None

            cur_track += delta
            if cur_track == 0 or cur_track > self.MAX_TRACK:
                # end of disk
                cur_sector = 0
                tries -= 1
                if tries:
                    # try other side of directory
                    delta = -delta
                    cur_track = self.DIR_TRACK + delta
                else:
                    # tried either side of the directory, try directory track
                    cur_track = self.DIR_TRACK

    @classmethod
    def create(cls, filepath, disk_name, disk_id):
        """Create an empty disk image."""
        empty = bytes(174848)
        with filepath.open('wb') as fh:
            fh.write(empty)

        image = cls(filepath)
        try:
            image.open('r+b')

            # block 18/0 contains the BAM and various identifying fields
            bam_block = Block(image, cls.DIR_TRACK, 0)
            image.dos_version = 0x41
            bam_block.set(0x90, b'\xa0' * 0x1b)
            image.name = disk_name
            image.id = disk_id
            image.dos_type = b'2A'

            # populate the BAM with all free blocks
            for sectors, range_ in cls.TRACK_SECTOR_MAX:
                for t in range(range_[0], range_[1]+1):
                    bits_free = '1' * sectors
                    image.bam.set_entry(t, sectors, bits_free)

            # block 18/1 contains 8 empty directory entries
            dir_block = Block(image, cls.DIR_TRACK, 1)
            dir_block.data_size = 0xfe

            # link BAM block to directory block
            bam_block.set_next_block(dir_block)

            # allocate both blocks
            image.bam.set_allocated(cls.DIR_TRACK, 0)
            image.bam.set_allocated(cls.DIR_TRACK, 1)
        finally:
            image.close()
