from base64 import b64decode
from base64 import b64encode
from io import StringIO

from Crypto import Random
from Crypto.Cipher import PKCS1_v1_5
from Crypto.Hash import SHA
from Crypto.PublicKey import RSA


def cid_decrypt(encrypted_cid, private_key):
    key = RSA.importKey(b64decode(private_key))
    dsize = SHA.digest_size
    sentinel = Random.new().read(15+dsize)
    cipher = PKCS1_v1_5.new(key)
    message = cipher.decrypt(b64decode(encrypted_cid), sentinel)
    return message


def cid_encrypt(cid, public_key):
    pubkey = RSA.importKey(b64decode(public_key))
    cipher = PKCS1_v1_5.new(pubkey)

    # without padding digest
    message = b64encode(cipher.encrypt(cid.encode('utf-8')))

    # with padding digest
    #h = SHA.new(cid.encode('utf-8'))
    #print(h.digest())
    #message = b64encode(cipher.encrypt((cid).encode('utf-8') + h.digest()))

    return message
