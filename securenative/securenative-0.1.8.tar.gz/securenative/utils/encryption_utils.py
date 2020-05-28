import json
from binascii import unhexlify, hexlify
from json import JSONDecodeError

from Crypto import Random
from Crypto.Cipher import AES

from securenative.models.client_token import ClientToken


class EncryptionUtils(object):
    BLOCK_SIZE = 16
    KEY_SIZE = 32

    @classmethod
    def encrypt(cls, text, cipher_key):
        key = cipher_key[:cls.KEY_SIZE]
        iv = Random.new().read(AES.block_size)
        cipher = AES.new(key, AES.MODE_CBC, iv)
        raw = str(cls._pad(text))
        return hexlify(iv + cipher.encrypt(raw))

    @classmethod
    def decrypt(cls, encrypted, cipher_key):
        key = cipher_key[:cls.KEY_SIZE]
        content = unhexlify(encrypted)
        iv = content[:cls.BLOCK_SIZE]
        cipher_text = content[cls.BLOCK_SIZE:]
        aes = AES.new(key, AES.MODE_CBC, iv)
        rv = aes.decrypt(cipher_text).decode("utf-8").strip()
        try:
            secret = json.loads(rv)
            return ClientToken(secret.get("cid"), secret.get("vid"), secret.get("fp"))
        except JSONDecodeError:
            return rv

    @classmethod
    def _pad(cls, s):
        return lambda s: s + (cls.BLOCK_SIZE - len(s) % cls.BLOCK_SIZE) * chr(cls.BLOCK_SIZE - len(s) % cls.BLOCK_SIZE)

