#coding=utf-8
from Crypto import Random
from Crypto.Cipher import PKCS1_v1_5 as Cipher_pkcs1_v1_5
from Crypto.PublicKey import RSA
import base64

# 伪随机数生成器
random_generator = Random.new().read
# rsa算法生成实例
rsa = RSA.generate(1024, random_generator)
#生成私钥
private_pem = rsa.exportKey()
print(private_pem)

#master-private.pem文件中写入私钥
# with open('master-private.pem', 'w') as f:
#     f.write(private_pem)
fout = open('master-private.pem', 'w', encoding='utf8')
fout.write(private_pem)
fout.close()

#生成公钥
public_pem = rsa.publickey().exportKey()
#master-public.pem公钥写入文件中
# with open('master-public.pem', 'w') as f:
#     f.write(public_pem)
fout2 = open('master-public.pem', 'w', encoding='utf8')
fout2.write(private_pem)
fout2.close()


if __name__=='__main__':
    message = 'hello world !'
    #将明文加密成密文
    with open('master-public.pem') as f:
        key = f.read()
        rsakey = RSA.importKey(key)
        cipher = Cipher_pkcs1_v1_5.new(rsakey)
        cipher_text = base64.b64encode(cipher.encrypt(message))
        print('hello world!对应的密文是：', cipher_text)

    #将密文解密成明文
    with open('master-private.pem') as f:
        key = f.read()
        rsakey = RSA.importKey(key)
        cipher = Cipher_pkcs1_v1_5.new(rsakey)
        text = cipher.decrypt(base64.b64decode(cipher_text), 'azx')
        print('解密后原文是:', text)

