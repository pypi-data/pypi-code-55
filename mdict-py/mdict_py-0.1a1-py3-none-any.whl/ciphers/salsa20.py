from struct import Struct


class Salsa20:
    little_u64 = Struct('<Q')
    little16_i32 = Struct('<16i')
    little4_i32 = Struct('<4i')
    little2_i32 = Struct('<2i')

    def __init__(self, key=None, iv=None, rounds=20):
        self.__last_chunk64__ = True
        self.__iv_bit_length__ = 64
        self.ctx = [0] * 16
        if key:
            self.__set_key__(key)
        if iv:
            self.__set_iv__(iv)
        self.__set_rounds__(rounds)

    def __set_key__(self, key):
        assert type(key) == bytes
        ctx = self.ctx
        if len(key) == 32:
            constants = b'expand 32-byte k'
            ctx[1], ctx[2], ctx[3], ctx[4] = Salsa20.little4_i32.unpack(key[0:16])
            ctx[11], ctx[12], ctx[13], ctx[14] = Salsa20.little4_i32.unpack(key[16:32])
        elif len(key) == 16:
            constants = b'expand 16-byte k'
            ctx[1], ctx[2], ctx[3], ctx[4] = Salsa20.little4_i32.unpack(key[0:16])
            ctx[11], ctx[12], ctx[13], ctx[14] = Salsa20.little4_i32.unpack(key[0:16])
        else:
            raise Exception("key length isn't 32 or 16 bytes.")
        ctx[0], ctx[5], ctx[10], ctx[15] = Salsa20.little4_i32.unpack(constants)

    def __set_iv__(self, iv):
        assert type(iv) == bytes
        assert len(iv) * 8 == 64, 'nonce (iv) not 64 bits'
        self.iv = iv
        ctx = self.ctx
        ctx[6], ctx[7] = Salsa20.little2_i32.unpack(iv)
        ctx[8], ctx[9] = 0, 0

    def __set_nonce__(self, iv):
        return self.__set_iv__(iv)

    def __set_counter__(self, counter):
        assert isinstance(counter, int)
        assert 0 <= counter < 1 << 64, 'counter < 0 or >= 2**64'
        ctx = self.ctx
        ctx[8], ctx[9] = Salsa20.little2_i32.unpack(Salsa20.little_u64.pack(counter))

    def __get_counter__(self):
        return Salsa20.little_u64.unpack(Salsa20.little2_i32.pack(*self.ctx[8:10]))[0]

    def __set_rounds__(self, rounds, testing=False):
        assert testing or rounds in [8, 12, 20], 'rounds must be 8, 12, 20'
        self.rounds = rounds

    def encrypt(self, data):
        assert type(data) == bytes, 'data must be byte string'
        assert self.__last_chunk64__, 'previous chunk not multiple of 64 bytes'
        data_length = len(data)
        munged = bytearray(data_length)
        for i in range(0, data_length, 64):
            h = self.salsa20_word_to_byte(self.ctx, self.rounds, check_rounds=False)
            self.__set_counter__((self.__get_counter__() + 1) % 2 ** 64)
            for j in range(min(64, data_length - i)):
                munged[i + j] = data[i + j] ^ h[j]

        self.__last_chunk64__ = not data_length % 64
        return bytes(munged)

    def decrypt(self, data):
        return self.encrypt(data)

    @staticmethod
    def salsa20_word_to_byte(input_data, n_rounds=20, check_rounds=True):
        assert type(input_data) in (list, tuple) and len(input_data) == 16
        assert not check_rounds or (n_rounds in [8, 12, 20])

        x = list(input_data)

        XOR = Salsa20.xor
        ROTATE = Salsa20.rot32
        PLUS = Salsa20.add32

        for i in range(n_rounds // 2):
            x[4] = XOR(x[4], ROTATE(PLUS(x[0], x[12]), 7))
            x[8] = XOR(x[8], ROTATE(PLUS(x[4], x[0]), 9))
            x[12] = XOR(x[12], ROTATE(PLUS(x[8], x[4]), 13))
            x[0] = XOR(x[0], ROTATE(PLUS(x[12], x[8]), 18))
            x[9] = XOR(x[9], ROTATE(PLUS(x[5], x[1]), 7))
            x[13] = XOR(x[13], ROTATE(PLUS(x[9], x[5]), 9))
            x[1] = XOR(x[1], ROTATE(PLUS(x[13], x[9]), 13))
            x[5] = XOR(x[5], ROTATE(PLUS(x[1], x[13]), 18))
            x[14] = XOR(x[14], ROTATE(PLUS(x[10], x[6]), 7))
            x[2] = XOR(x[2], ROTATE(PLUS(x[14], x[10]), 9))
            x[6] = XOR(x[6], ROTATE(PLUS(x[2], x[14]), 13))
            x[10] = XOR(x[10], ROTATE(PLUS(x[6], x[2]), 18))
            x[3] = XOR(x[3], ROTATE(PLUS(x[15], x[11]), 7))
            x[7] = XOR(x[7], ROTATE(PLUS(x[3], x[15]), 9))
            x[11] = XOR(x[11], ROTATE(PLUS(x[7], x[3]), 13))
            x[15] = XOR(x[15], ROTATE(PLUS(x[11], x[7]), 18))

            x[1] = XOR(x[1], ROTATE(PLUS(x[0], x[3]), 7))
            x[2] = XOR(x[2], ROTATE(PLUS(x[1], x[0]), 9))
            x[3] = XOR(x[3], ROTATE(PLUS(x[2], x[1]), 13))
            x[0] = XOR(x[0], ROTATE(PLUS(x[3], x[2]), 18))
            x[6] = XOR(x[6], ROTATE(PLUS(x[5], x[4]), 7))
            x[7] = XOR(x[7], ROTATE(PLUS(x[6], x[5]), 9))
            x[4] = XOR(x[4], ROTATE(PLUS(x[7], x[6]), 13))
            x[5] = XOR(x[5], ROTATE(PLUS(x[4], x[7]), 18))
            x[11] = XOR(x[11], ROTATE(PLUS(x[10], x[9]), 7))
            x[8] = XOR(x[8], ROTATE(PLUS(x[11], x[10]), 9))
            x[9] = XOR(x[9], ROTATE(PLUS(x[8], x[11]), 13))
            x[10] = XOR(x[10], ROTATE(PLUS(x[9], x[8]), 18))
            x[12] = XOR(x[12], ROTATE(PLUS(x[15], x[14]), 7))
            x[13] = XOR(x[13], ROTATE(PLUS(x[12], x[15]), 9))
            x[14] = XOR(x[14], ROTATE(PLUS(x[13], x[12]), 13))
            x[15] = XOR(x[15], ROTATE(PLUS(x[14], x[13]), 18))

        for i in range(len(input_data)):
            x[i] = PLUS(x[i], input_data[i])
        return Salsa20.little16_i32.pack(*x)

    @staticmethod
    def xor(a, b):
        return a ^ b

    @staticmethod
    def trunc32(w):
        w = int((w & 0x7fffFFFF) | -(w & 0x80000000))
        assert type(w) == int
        return w

    @staticmethod
    def add32(a, b):
        lo = (a & 0xFFFF) + (b & 0xFFFF)
        hi = (a >> 16) + (b >> 16) + (lo >> 16)
        return (-(hi & 0x8000) | (hi & 0x7FFF)) << 16 | (lo & 0xFFFF)

    @staticmethod
    def rot32(w, n_left):
        n_left &= 31
        if n_left == 0:
            return w
        RRR = (((w >> 1) & 0x7fffFFFF) >> (31 - n_left))
        s_llllll = -((1 << (31 - n_left)) & w) | (0x7fffFFFF >> n_left) & w
        return RRR | (s_llllll << n_left)
