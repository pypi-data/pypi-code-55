# -*- coding: utf-8 -*-

import base64
import rsa

publicKey = "MIGfMA0GCSqGSIb3DQEBAQUAA4GNADCBiQKBgQCylvPMI6QHoNmAOt0Pb+ONACaobN6LV65F9NnzjGugUFd1nwc4QJyfvn1sWYLvZi1zBw5Lbx1xDaBPazaz73JGu8ugyhIMr4V/dY7b4GKtMfwMMgGoEChigYlTRXeWR1suzIMxyMLsp8LUqyjfY6ebJa2L9niun0t7P4E7MaLTIQIDAQAB"
privateKey = "MIICdgIBADANBgkqhkiG9w0BAQEFAASCAmAwggJcAgEAAoGBALKW88wjpAeg2YA63Q9v440AJqhs3otXrkX02fOMa6BQV3WfBzhAnJ++fWxZgu9mLXMHDktvHXENoE9rNrPvcka7y6DKEgyvhX91jtvgYq0x/AwyAagQKGKBiVNFd5ZHWy7MgzHIwuynwtSrKN9jp5slrYv2eK6fS3s/gTsxotMhAgMBAAECgYBlF8IF6p7tmoXEao28MVAT/uPjL02Cfy2td/7wOKqr4w6/DDhgBWMjogcJkFnn/mT32iSjWtDFsDrw+fXLQV3j7lDFO+i3ubGXpYPBg+8DzpzSksU8/AYT0+vbDAfkAePcMfDTBToqg/n87USc+7zMnKtboVzjkbBtveWOto3WqQJBANe9Kenrwm6r2u+H1YzZ3rqLbWQq1yhqvY0XLv1BlRVNCwJfSIZ5Y4qGvgyT05F4lKK1HfZO2KbO2zRUl9qn4PcCQQDT6v+H/MAutMiz70P+Gc3458lF/pC/h8PiMF823r0oHoV2cTgljv/N4z5Gkxk0suFnU6BiV5gtpj1uZYlZ5v6nAkAPcS/V2ZVCPLTgHlXvzgx+R8qdt99Muk81ESrA3/fe3XPjSJS1Y2z3lmt2FQK4z+u7tcEeR0iEsBvKpB92fDvDAkBsZT2DX2MmAM7QSshqhuR2NokbRlTfwyAM6FUric8TYFk/9jWT8Isj0uKd0swHyp/E7F+TLd7nKqstdr5EwATtAkEAy3VYpUOW5XoIsFQvd5oTcSC+L8sY2FyMyUooXmfXOAnw5hZp2fVG1bIsVMDbYfkH1cDec3DLuTHVKTYYWy3zNQ=="
content = "aWKmYUQ3whFj2KyRd5npX3zGH+EzcF8EYgHGl32ExwPRwsVUk0OG2DtJ3hTUTmzfJQwhdO/ec/GzF5q8AHZjWoDNlw/0yDQghDDAlMQ0V9SBYWnkXqoI0oyRas4KU/psPmimabB4u4NoLmVX5RV243/jpMjpaashLMOjTl8BaxQaPjW4+wKCH4pPJWfdpQ0WesUVNk1vq/vYtGfb326F4sIxiF26MfmnrnoCohvYU9SfRiZ/eP8hGBLlUH4lplhYQSJwvZP/Y0KVsHw0lHxa+T6nd+uy0uFt8i3/1mWTFqvsiOZgg7I/JRsLCVw3FxerKVKGg3oi9Dj2yYhzgpvFPE0QGiqbMsBO1WaQxw1ZocEUx7OboNtfdMyhZf+Jq316KbKe1XIKUCKWBbJpKxMefmDBRkyUGkNCb7uHAF0ANPISnyHFdK+428qUZL6hlH1cXkhDKw+noEr0/BpQe3YAngNQM0jZGXR9wewTU7L9zrf2Oun4i8P8zgSsj/hPYMfalLcP3NR0G0flVZzbftaMI7ZXh8nm20BAI/Gv0lBU8pW1kMnrHlm+gPt8Bjkfpocel+QOpVOicDeYx2sBAmBNx4ux2TvPSmFHePSqMAffzkPLICTGD3e/ckLovWeixIp5kcZNDWWj7O5/WPRsXu+AK6muyOHLzhaxD1NmknQ6FBxneSDC5X9b+VyMHkjDN+VVBwL+ZnnZcLWRR6hhi1W03hJkYRbmJSD0cQMVYIksZHJcR62P78jMqq4+TG73VMDKEEGnF/YaUoc2bgfYpz1KPQOFZ1ALXcm4mB/2agodKLikN5DRr5YuJtUlCmIF2WhobcYrvQDTqNjImb52pWv2Lg=="
private_key_pem ="""-----BEGIN RSA PRIVATE KEY-----
%s
-----END RSA PRIVATE KEY-----""" %base64.b64decode(privateKey)
public_key_pem ="""-----BEGIN RSA PUBLIC KEY-----
%s
-----END RSA PUBLIC KEY-----""" %publicKey

# import base64
# plaintext="明文"
# ciphertext = base64.b64encode(plaintext)
# plaintext = base64.b64decode(ciphertext)

# import rsa
# plaintext="明文"
# ciphertext = rsa.encrypt(plaintext, publicKey)
# plaintext = rsa.decrypt(ciphertext, privateKey)
(pubkey, privkey) = rsa.newkeys(1024)
pub = pubkey.save_pkcs1()
pubfile = open('public.pem','wb')
pubfile.write(pub)
pubfile.close()
pri = privkey.save_pkcs1()
prifile = open('private.pem','wb')
prifile.write(pri)
prifile.close()


# load公钥和密钥
message = 'lovesoo.org'
with open('public.pem') as publickfile:
  p = publickfile.read()
  pubkey = rsa.PublicKey.load_pkcs1(p)
with open('private.pem') as privatefile:
  p = privatefile.read()
  privkey = rsa.PrivateKey.load_pkcs1(p)
# 用公钥加密、再用私钥解密
crypto = rsa.encrypt(message, pubkey)
message = rsa.decrypt(crypto, privkey)
print(message)
# sign 用私钥签名认证、再用公钥验证签名
signature = rsa.sign(message, privkey, 'SHA-1')
rsa.verify('lovesoo.org', signature, pubkey)






class mydecry(object):
    #构造方法传入私钥
    def __init__(self,private_key_pem):
        self.private_key_pem = private_key_pem
        # private_key_pem_encode =  base64.b64decode(privateKey)
        self.pk = rsa.PrivateKey.load_pkcs1(private_key_pem)
        print(self.pk )

    def decry_str(self,miwen):
        bit_miwen = base64.b64decode(miwen)
        mingwen = rsa.decrypt(bit_miwen, self.pk)
        return mingwen