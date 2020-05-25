import zlib
from struct import pack, unpack
from .mdict import MDict
try:
    import lzo
except ImportError:
    lzo = None


class MDD(MDict):
    def __init__(self, filename, pass_code=None):
        MDict.__init__(self, filename, encoding='UTF-16', pass_code=pass_code)

    def items(self):
        return self.__decode_record_block__()

    def __decode_record_block__(self):
        file = open(self.__filename__, 'rb')
        file.seek(self.__record_block_offset__)

        num_record_blocks = self.__read_number__(file)
        num_entries = self.__read_number__(file)
        assert num_entries == self.__num_entries__
        record_block_info_size = self.__read_number__(file)
        record_block_size = self.__read_number__(file)

        # record block info section
        record_block_info_list = []
        size_counter = 0
        for i in range(num_record_blocks):
            compressed_size = self.__read_number__(file)
            decompressed_size = self.__read_number__(file)
            record_block_info_list += [(compressed_size, decompressed_size)]
            size_counter += self.__number_width__ * 2
        assert size_counter == record_block_info_size

        # actual record block
        offset = 0
        i = 0
        size_counter = 0
        for compressed_size, decompressed_size in record_block_info_list:
            record_block_compressed = file.read(compressed_size)
            # 4 bytes: compression type
            record_block_type = record_block_compressed[:4]
            # 4 bytes: adler32 checksum of decompressed record block
            adler32 = unpack('>I', record_block_compressed[4:8])[0]
            if record_block_type == b'\x00\x00\x00\x00':
                record_block = record_block_compressed[8:]
            elif record_block_type == b'\x01\x00\x00\x00':
                if lzo is None:
                    break
                # decompress
                header = b'\xf0' + pack('>I', decompressed_size)
                record_block = lzo.decompress(header + record_block_compressed[8:])
            elif record_block_type == b'\x02\x00\x00\x00':
                # decompress
                record_block = zlib.decompress(record_block_compressed[8:])

            # notice that adler32 return signed value
            assert adler32 == zlib.adler32(record_block) & 0xffffffff

            assert len(record_block) == decompressed_size
            # split record block according to the offset info from key block
            while i < len(self.__key_list__):
                record_start, key_text = self.__key_list__[i]
                # reach the end of current record block
                if record_start - offset >= len(record_block):
                    break
                # record end index
                if i < len(self.__key_list__) - 1:
                    record_end = self.__key_list__[i+1][0]
                else:
                    record_end = len(record_block) + offset
                i += 1
                data = record_block[record_start-offset:record_end-offset]
                yield key_text, data
            offset += len(record_block)
            size_counter += compressed_size
        assert size_counter == record_block_size

        file.close()
