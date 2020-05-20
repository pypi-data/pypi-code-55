import base64
import random

from .easy_aes import EasyAES
from ...share.log import logger


class TokenHelper:

    secret = None
    magic = None

    # 分割符
    split_bytes = b','

    block_size = 16

    def __init__(self, secret, magic):
        """
        secret: AES key,  must be either 16, 24, or 32 bytes long
        magic: 作用是为了检测解密是否正确
        """
        self.secret = self._force_convert_to_bytes(secret)
        self.magic = self._force_convert_to_bytes(magic)

    def encode(self, *args):
        """
        1. 拼源串src，格式为 magic, *args，以split_bytes分隔。
        2. 使用aes_cbc方法将源串src加密成串dst
        3. 之后将iv与dst拼成token。
            token的格式为 前16位 固定为iv，剩下的部分为token。

        4. 之后将token进行base64加密方便http传输

        :param args:
        :return: 加密后字符串。为方便传输，类型为str。
        """
        iv = self._force_convert_to_bytes(self._gen_rand_str(self.block_size))

        aes = EasyAES(
            self.secret,
            iv
        )

        params = [self.magic]
        for it in args:
            params.append(self._force_convert_to_bytes(it))

        src = self.split_bytes.join(params)

        en_str = aes.encrypt(src)

        packed_str = iv + en_str

        base64_result = base64.b64encode(packed_str)

        return base64_result.decode('utf8')

    def decode(self, token):
        """
        解析token
        :param token:
        :return: 被加密的数组。与encode时一样的顺序，类型都是bytes。
        """

        packed_src = base64.b64decode(token)

        iv = packed_src[:self.block_size]
        en_src = packed_src[self.block_size:]

        aes = EasyAES(
            self.secret,
            iv
        )

        de_src = aes.decrypt(en_src)

        if not de_src:
            logger.info('decrypt fail. token: %s', token)
            return None

        values = de_src.split(self.split_bytes)

        # 第一个是magic
        magic = values.pop(0)
        if magic != self.magic:
            logger.info('invalid magic. token: %s', token)
            return None

        return values

    def _gen_rand_str(self, length):
        """
        generate secret key，参考django
        不区分大小写，因为mysql的unique不区分大小写
        """
        chars = 'abcdefghijklmnopqrstuvwxyz0123456789!@#$%^&*(-_=+)'
        return ''.join([random.choice(chars) for i in range(length)])

    def _force_convert_to_bytes(self, src):
        """
        强制转换为bytes
        bytes => bytes
        str => bytes
        else => str => bytes
        """

        if isinstance(src, bytes):
            return src
        elif isinstance(src, str):
            return bytes(src, encoding='utf8')
        else:
            return bytes(str(src), encoding='utf8')
