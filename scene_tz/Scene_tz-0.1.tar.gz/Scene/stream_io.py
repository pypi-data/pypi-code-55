import struct


class StreamIO:
    def debug(self, string):
        if self.is_debug:
            print(string)

    def __init__(self, stream, is_debug=False):
        self.stream = stream
        self.is_debug = is_debug

    def write_boolean(self, boolean):
        self.stream.write(struct.pack('?', boolean))

    def read_boolean(self):
        return bool(struct.unpack('?', self.stream.read(1))[0])

    def write_double(self, val):
        self.stream.write(struct.pack('d', val))

    def read_double(self):
        fmt = 'd'
        size = struct.calcsize(fmt)
        return float(struct.unpack('d', self.stream.read(size))[0])

    def read_real48(self):
        r48 = [self.read_char() for _ in range(6)][::-1]

        '''Return value of r48 - explicit calculation.

        Algorithm 'stolen' and adapted from:
          program sixbytes { jrs at merlyn.demon.co.uk  >= 2001-11-25 } ;
        at http://www.merlyn.demon.co.uk/pas-type.htm#FF
        '''
        a0, a1, a2 = ord(r48[0]), ord(r48[1]), ord(r48[2])
        a3, a4, a5 = ord(r48[3]), ord(r48[4]), ord(r48[5])
        sign = a0 / 128
        exp = a5 - 129
        # Q = 1.0/256  # Q / R2 = alternative
        if a5 == 0:
            r1 = 0.0
            # R2 = 0.0
        else:
            r1 = 1.0 + 2.0 * ((a0 %
                               128) + (a1 + (a2 + (a3 + a4 / 256.0) / 256.0) / 256.0) / 256.0) / 256.0
            # R2 = 1.0 + 2.0 * ((((a4*Q+a3)*Q+a2)*Q+a1)*Q+(a0 % 128))*Q
        if sign:
            r1 = -r1
            # R2 = -R2
        # info_tuple = sign, exp, 2.0**exp * R1, R1, R2
        result = 2.0 ** exp * r1
        return result

    def write_int16(self, val):
        self.stream.write(struct.pack('h', val))

    def read_int16(self):
        return int(struct.unpack('h', self.stream.read(2))[0])

    def write_word(self, val):
        self.stream.write(struct.pack('H', val))

    def read_word(self):
        return int(struct.unpack('H', self.stream.read(2))[0])

    def write_unsigned_byte(self, val):
        self.stream.write(struct.pack('B', val))

    def read_unsigned_byte(self):
        return int(struct.unpack('B', self.stream.read(1))[0])

    def write_string(self, string):
        self.write_unsigned_byte(len(string))
        self.stream.write(string)

    def read_string(self, length):
        data_len = self.read_unsigned_byte()
        data = self.stream.read(length)

        return data[:data_len]

    def write_char(self, char):
        self.stream.write(struct.pack('c', char))

    def read_char(self):
        return struct.unpack('c', self.stream.read(1))[0]

    def write_utf(self, string):
        self.write_string(string)

    def read_utf(self, length):
        data_len = self.read_unsigned_byte()
        data = self.stream.read(length - 1)

        # print(data[:data_len])

        return data[:data_len]
