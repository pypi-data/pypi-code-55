import re
import zlib
import sys
from struct import pack, unpack
from io import BytesIO
from ..ciphers import Ripemd128, Salsa20
try:
    import lzo
except ImportError:
    lzo = None


class MDict:
    def __init__(self, filename, encoding='', pass_code=None):
        self.__filename__ = filename
        self.__encoding__ = encoding.upper()
        self.__pass_code__ = pass_code

        self.__header__ = self.__read_header__()
        try:
            self.__key_list__ = self.__read_keys__()
        except AssertionError:
            self.__key_list__ = self.__read_keys_brutal__()

    @property
    def filename(self):
        return self.__filename__

    @property
    def encoding(self):
        return self.__encoding__.lower()

    @property
    def pass_code(self):
        return self.__pass_code__

    @property
    def header(self):
        return self.__header__

    @property
    def version(self):
        return self.__version__

    @property
    def encrypt(self):
        return self.__encrypt__

    @staticmethod
    def __unescape_entities__(text):
        text = text.replace(b'&lt;', b'<')
        text = text.replace(b'&gt;', b'>')
        text = text.replace(b'&quot;', b'"')
        text = text.replace(b'&amp;', b'&')
        return text

    @staticmethod
    def __fast_decrypt__(data, key):
        b = bytearray(data)
        key = bytearray(key)
        previous = 0x36
        for i in range(len(b)):
            t = (b[i] >> 4 | b[i] << 4) & 0xff
            t = t ^ previous ^ (i & 0xff) ^ key[i % len(key)]
            previous = b[i]
            b[i] = t
        return bytes(b)

    @staticmethod
    def __mdx_decrypt__(comp_block):
        key = Ripemd128.hash(comp_block[4:8] + pack(b'<L', 0x3695))
        return comp_block[0:8] + MDict.__fast_decrypt__(comp_block[8:], key)

    @staticmethod
    def __salsa_decrypt__(cipher_text, encrypt_key):
        s20 = Salsa20(key=encrypt_key, iv=b'\x00'*8, rounds=8)
        return s20.encrypt(cipher_text)

    @staticmethod
    def __decrypt_reg_code_by_device_id__(reg_code, device_id):
        device_id_digest = Ripemd128.hash(device_id)
        s20 = Salsa20(key=device_id_digest, iv=b'\x00'*8, rounds=8)
        encrypt_key = s20.encrypt(reg_code)
        return encrypt_key

    @staticmethod
    def _decrypt_reg_code_by_email(reg_code, email):
        email_digest = Ripemd128.hash(email.decode().encode('utf-16-le'))
        s20 = Salsa20(key=email_digest, iv=b'\x00'*8, rounds=8)
        encrypt_key = s20.encrypt(reg_code)
        return encrypt_key

    def __len__(self):
        return self.__num_entries__

    def __iter__(self):
        return self.keys()

    def keys(self):
        return list(key_value for key_id, key_value in self.__key_list__)

    def __read_number__(self, f):
        return unpack(self.__number_format__, f.read(self.__number_width__))[0]

    @staticmethod
    def __parse_header__(header):
        tag_list = re.findall(rb'(\w+)="(.*?)"', header, re.DOTALL)
        tag_dict = dict()
        for key, value in tag_list:
            tag_dict[key] = MDict.__unescape_entities__(value)
        return tag_dict

    def __decode_key_block_info__(self, key_block_info_compressed):
        if self.__version__ >= 2:
            assert key_block_info_compressed[:4] == b'\x02\x00\x00\x00'
            if self.__encrypt__ & 0x02:
                key_block_info_compressed = MDict.__mdx_decrypt__(key_block_info_compressed)
            key_block_info = zlib.decompress(key_block_info_compressed[8:])
            adler32 = unpack('>I', key_block_info_compressed[4:8])[0]
            assert adler32 == zlib.adler32(key_block_info) & 0xffffffff
        else:
            key_block_info = key_block_info_compressed
        key_block_info_list = []
        num_entries = 0
        i = 0
        if self.__version__ >= 2:
            byte_format = '>H'
            byte_width = 2
            text_term = 1
        else:
            byte_format = '>B'
            byte_width = 1
            text_term = 0

        while i < len(key_block_info):
            num_entries += unpack(self.__number_format__, key_block_info[i:i + self.__number_width__])[0]
            i += self.__number_width__
            text_head_size = unpack(byte_format, key_block_info[i:i + byte_width])[0]
            i += byte_width
            if self.__encoding__ != 'UTF-16':
                i += text_head_size + text_term
            else:
                i += (text_head_size + text_term) * 2
            text_tail_size = unpack(byte_format, key_block_info[i:i + byte_width])[0]
            i += byte_width
            if self.__encoding__ != 'UTF-16':
                i += text_tail_size + text_term
            else:
                i += (text_tail_size + text_term) * 2
            key_block_compressed_size = unpack(self.__number_format__, key_block_info[i:i + self.__number_width__])[0]
            i += self.__number_width__
            key_block_decompressed_size = unpack(self.__number_format__, key_block_info[i:i + self.__number_width__])[0]
            i += self.__number_width__
            key_block_info_list += [(key_block_compressed_size, key_block_decompressed_size)]

        return key_block_info_list

    def __decode_key_block__(self, key_block_compressed, key_block_info_list):
        key_list = []
        i = 0
        for compressed_size, decompressed_size in key_block_info_list:
            start = i
            end = i + compressed_size
            key_block_type = key_block_compressed[start:start + 4]
            adler32 = unpack('>I', key_block_compressed[start + 4:start + 8])[0]
            if key_block_type == b'\x00\x00\x00\x00':
                key_block = key_block_compressed[start + 8:end]
            elif key_block_type == b'\x01\x00\x00\x00':
                if lzo is None:
                    break
                header = b'\xf0' + pack('>I', decompressed_size)
                key_block = lzo.decompress(header + key_block_compressed[start + 8:end])
            elif key_block_type == b'\x02\x00\x00\x00':
                key_block = zlib.decompress(key_block_compressed[start + 8:end])
            key_list += self.__split_key_block__(key_block)
            assert adler32 == zlib.adler32(key_block) & 0xffffffff
            i += compressed_size
        return key_list

    def __split_key_block__(self, key_block):
        key_list = []
        key_start_index = 0
        while key_start_index < len(key_block):
            key_id = unpack(self.__number_format__, key_block[key_start_index:key_start_index + self.__number_width__])[0]
            if self.__encoding__ == 'UTF-16':
                delimiter = b'\x00\x00'
                width = 2
            else:
                delimiter = b'\x00'
                width = 1
            i = key_start_index + self.__number_width__
            while i < len(key_block):
                if key_block[i:i + width] == delimiter:
                    key_end_index = i
                    break
                i += width
            key_text = key_block[key_start_index + self.__number_width__:key_end_index] \
                .decode(self.__encoding__, errors='ignore').encode('utf-8').strip()
            key_start_index = key_end_index + width
            key_list += [(key_id, key_text)]
        return key_list

    def __read_header__(self):
        f = open(self.__filename__, 'rb')
        header_bytes_size = unpack('>I', f.read(4))[0]
        header_bytes = f.read(header_bytes_size)
        adler32 = unpack('<I', f.read(4))[0]
        assert adler32 == zlib.adler32(header_bytes) & 0xffffffff
        self.__key_block_offset__ = f.tell()
        f.close()

        header_text = header_bytes[:-2].decode('utf-16').encode('utf-8')
        header_tag = MDict.__parse_header__(header_text)
        if not self.__encoding__:
            encoding = header_tag[b'Encoding']
            if sys.hexversion >= 0x03000000:
                encoding = encoding.decode('utf-8')
            if encoding in ['GBK', 'GB2312']:
                encoding = 'GB18030'
            self.__encoding__ = encoding
        if b'Encrypted' not in header_tag or header_tag[b'Encrypted'] == b'No':
            self.__encrypt__ = 0
        elif header_tag[b'Encrypted'] == b'Yes':
            self.__encrypt__ = 1
        else:
            self.__encrypt__ = int(header_tag[b'Encrypted'])

        self.__stylesheet__ = dict()
        if header_tag.get('StyleSheet'):
            lines = header_tag['StyleSheet'].splitlines()
            for i in range(0, len(lines), 3):
                self.__stylesheet__[lines[i]] = (lines[i + 1], lines[i + 2])

        self.__version__ = float(header_tag[b'GeneratedByEngineVersion'])
        if self.__version__ < 2.0:
            self.__number_width__ = 4
            self.__number_format__ = '>I'
        else:
            self.__number_width__ = 8
            self.__number_format__ = '>Q'

        return header_tag

    def __read_keys__(self):
        f = open(self.__filename__, 'rb')
        f.seek(self.__key_block_offset__)

        if self.__version__ >= 2.0:
            num_bytes = 8 * 5
        else:
            num_bytes = 4 * 4
        block = f.read(num_bytes)

        if self.__encrypt__ & 1:
            if self.__pass_code__ is None:
                raise RuntimeError('user identification is needed to read encrypted file')
            register_code, user_id = self.__pass_code__
            if isinstance(user_id, str):
                user_id = user_id.encode('utf8')
            if self.__header__[b'RegisterBy'] == b'EMail':
                encrypted_key = MDict._decrypt_reg_code_by_email(register_code, user_id)
            else:
                encrypted_key = MDict.__decrypt_reg_code_by_device_id__(register_code, user_id)
            block = MDict.__salsa_decrypt__(block, encrypted_key)

        sf = BytesIO(block)
        num_key_blocks = self.__read_number__(sf)
        self.__num_entries__ = self.__read_number__(sf)
        if self.__version__ >= 2.0:
            key_block_info_decomposition_size = self.__read_number__(sf)
        key_block_info_size = self.__read_number__(sf)
        key_block_size = self.__read_number__(sf)

        if self.__version__ >= 2.0:
            adler32 = unpack('>I', f.read(4))[0]
            assert adler32 == (zlib.adler32(block) & 0xffffffff)

        key_block_info = f.read(key_block_info_size)
        key_block_info_list = self.__decode_key_block_info__(key_block_info)
        assert num_key_blocks == len(key_block_info_list)

        key_block_compressed = f.read(key_block_size)
        key_list = self.__decode_key_block__(key_block_compressed, key_block_info_list)

        self.__record_block_offset__ = f.tell()
        f.close()
        return key_list

    def __read_keys_brutal__(self):
        f = open(self.__filename__, 'rb')
        f.seek(self.__key_block_offset__)

        if self.__version__ >= 2.0:
            num_bytes = 8 * 5 + 4
            key_block_type = b'\x02\x00\x00\x00'
        else:
            num_bytes = 4 * 4
            key_block_type = b'\x01\x00\x00\x00'
        block = f.read(num_bytes)

        key_block_info = f.read(8)
        if self.__version__ >= 2.0:
            assert key_block_info[:4] == b'\x02\x00\x00\x00'
        while True:
            fpos = f.tell()
            t = f.read(1024)
            index = t.find(key_block_type)
            if index != -1:
                key_block_info += t[:index]
                f.seek(fpos + index)
                break
            else:
                key_block_info += t

        key_block_info_list = self.__decode_key_block_info__(key_block_info)
        key_block_size = sum(list(zip(*key_block_info_list))[0])

        key_block_compressed = f.read(key_block_size)
        key_list = self.__decode_key_block__(key_block_compressed, key_block_info_list)

        self.__record_block_offset__ = f.tell()
        f.close()

        self.__num_entries__ = len(key_list)
        return key_list
