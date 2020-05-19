# -*- coding: utf-8 -*-
import os
import hashlib
import binascii
import base64
from Crypto.Cipher import AES
from . import strutils
from . import listutils


AES_BLOCK_SIZE = AES.block_size


def get_sha1prng_key(key):
    """
    encrypt key with SHA1PRNG
    same as java AES crypto key generator SHA1PRNG
    """
    key = strutils.force_bytes(key)
    print(key)
    signature = hashlib.sha1(key).digest()
    signature = hashlib.sha1(signature).digest()
    return signature[:16]

def get_md5_key(key):
    key = strutils.force_bytes(key)
    signature = hashlib.md5(key).digest()
    return signature

def padding_ansix923(value):
    padsize = AES.block_size - len(value) % AES.block_size
    return value + listutils.int_list_to_bytes([0] * (padsize -1)) + listutils.int_list_to_bytes([padsize])

def remove_padding_ansix923(value):
    padsize = strutils.char_force_to_int(value[-1])
    return value[:-1*padsize]

def padding_iso10126(value):
    padsize = AES.block_size - len(value) % AES.block_size
    return value + os.urandom(padsize-1) + listutils.int_list_to_bytes([padsize])

def remove_padding_iso10126(value):
    padsize = strutils.char_force_to_int(value[-1])
    return value[:-1*padsize]

def padding_pkcs5(value):
    padsize = AES.block_size - len(value) % AES.block_size
    value = value + listutils.int_list_to_bytes([padsize] * padsize)
    return value

def remove_padding_pkcs5(value):
    padsize = strutils.char_force_to_int(value[len(value) - 1])
    return value[:-1*padsize]


def encrypt(data, password):
    """AES encrypt with AES/ECB/Pkcs5padding/SHA1PRNG options
    """
    data_padded = padding_pkcs5(data)
    key = get_sha1prng_key(password)
    cipher = AES.new(key, AES.MODE_ECB)
    data_encrypted = cipher.encrypt(data_padded)
    return data_encrypted

def decrypt(data_encrypted, password):
    """AES decrypt with AES/ECB/Pkcs5padding/SHA1PRNG options
    """
    key = get_sha1prng_key(password)
    cipher = AES.new(key, AES.MODE_ECB)
    data_padded = cipher.decrypt(data_encrypted)
    data = remove_padding_pkcs5(data_padded)
    return data

def encrypt_and_base64encode(data, password):
    data = strutils.force_bytes(data)
    data_encrypted = encrypt(data, password)
    data_base64_encoded = base64.encodebytes(data_encrypted).decode()
    return strutils.join_lines(data_base64_encoded)

def decrypt_and_base64decode(text, password):
    text = strutils.force_bytes(text)
    data_encrypted = base64.decodebytes(text)
    data = decrypt(data_encrypted, password)
    return data

def encrypt_and_safeb64encode(data, password):
    data = strutils.force_bytes(data)
    data_encrypted = encrypt(data, password)
    data_safeb64_encoded = base64.urlsafe_b64encode(data_encrypted).decode()
    return strutils.join_lines(data_safeb64_encoded)

def decrypt_and_safeb64decode(text, password):
    text = strutils.force_bytes(text)
    data_encrypted = base64.urlsafe_b64decode(text)
    data = decrypt(data_encrypted, password)
    return data

def encrypt_and_hexlify(data, password):
    data = strutils.force_bytes(data)
    data_encrypted = encrypt(data, password)
    data_hexlified = binascii.hexlify(data_encrypted).decode()
    return data_hexlified

def decrypt_and_unhexlify(text, password):
    text = strutils.force_bytes(text)
    data_encrypted = binascii.unhexlify(text)
    data = decrypt(data_encrypted, password)
    return data
