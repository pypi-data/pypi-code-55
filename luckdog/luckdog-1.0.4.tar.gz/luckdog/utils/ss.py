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

#master-private.pem文件中写入私钥
with open('master-private.pem', 'w') as f:
    f.write(private_pem)
#生成公钥
public_pem = rsa.publickey().exportKey()
#master-public.pem公钥写入文件中
with open('master-public.pem', 'w') as f:
    f.write(public_pem)
if __name__=='__main__':
    message = 'hello world !'
    #将明文加密成密文
    with open('master-public.pem') as f:
        key = f.read()
        rsakey = RSA.importKey(key)
        cipher = Cipher_pkcs1_v1_5.new(rsakey)
        cipher_text = base64.b64encode(cipher.encrypt(message))
        print 'hello world!对应的密文是：',cipher_text
    #将密文解密成明文
    with open('master-private.pem') as f:
        key = f.read()
        rsakey = RSA.importKey(key)
        cipher = Cipher_pkcs1_v1_5.new(rsakey)
        text = cipher.decrypt(base64.b64decode(cipher_text), 'azx')
        print '解密后原文是:',text



#coding=utf-8
from Crypto.PublicKey import RSA as rsa
from Crypto.Cipher import PKCS1_v1_5
import base64
class myencry(object):
    #构造方法传入公钥
    def __init__(self,pub_key_str=None):
        self.pub_key_str = """-----BEGIN RSA PUBLIC KEY-----
%s
-----END RSA PUBLIC KEY-----""" %pub_key_str
    #设置公钥
    def set_pk(self,pub_key_str):
        self.pub_key_str="""-----BEGIN RSA PUBLIC KEY-----
%s
-----END RSA PUBLIC KEY-----""" %pub_key_str
    #获取公钥
    def get_pk(self):
        return self.pub_key_str
    #获取加密对象
    def get_pubobj(self):
        pub_key_str=self.get_pk()
        pubobj = rsa.importKey(pub_key_str)
        pubobj = PKCS1_v1_5.new(pubobj)
        return pubobj
    #对用户名进行加密
    def get_encry_str(self,mingwen):
        encry_name = self.get_pubobj().encrypt(mingwen)
        miwen = base64.b64encode(encry_name)
        return miwen
if __name__=='__main__':
    pk='MIGfMA0GCSqGSIb3DQEBAQUAA4GNADCBiQKBgQDgDq5fGYiRqDQyfDYiFuBVUHukaK9zQ/6EPzG0O8bf+sEVuuiiWDSrjMaM28GNZWuxQRu1JOXkq3pFgULvWdqDUr6dl3ucmW4O0xpTMOQaz0iwaUIJnWhg0blgmj+eA+ZHj51rdVBKfuOCOWE4QpJc5igtnOrGHEFPpi/Lg+c5hwIDAQAB'
    en=myencry(pk)
    # en.set_pk(pk)
    print en.get_encry_str('596579936@qq.com')
    print en.get_encry_str('bAOBAO521')

#coding=utf-8
from Crypto.PublicKey import RSA as rsa
from Crypto.Cipher import PKCS1_v1_5
import base64
import random
class mydecry(object):
    #构造方法传入私钥
    def __init__(self,private_key):
        self.private_key="""-----BEGIN RSA PRIVATE KEY-----
%s
-----END RSA PRIVATE KEY-----""" %private_key
        self.pk=private_key
    #获取私钥
    def get_key(self):
        return self.private_key
    def set_key(self,private_key):
        self.private_key="""-----BEGIN RSA PRIVATE KEY-----
%s
-----END RSA PRIVATE KEY-----""" %private_key
        self.pk=private_key
    #获取解密对象
    def get_cipher(self):
        pri_key_str=self.get_key()
        rsakey = rsa.importKey(pri_key_str)
        cipher = PKCS1_v1_5.new(rsakey)
        return cipher
    #获取随机数
    def get_random(self):
        index=random.random()
        return str(index)
    #获取解密后的明文
    def get_decry_str(self,miwen):
        cipher=self.get_cipher()
        mingwen = cipher.decrypt(base64.b64decode(miwen), self.get_random())
        return mingwen
if __name__=="__main__":
    from myEncry import myencry
    private_key='MIICdgIBADANBgkqhkiG9w0BAQEFAASCAmAwggJcAgEAAoGBAJF4ZQGUjeueZIaY5+HgEAr7leBvP8/ftemF+eaNzl5PRF7rf3wIeoC7x1QzOPBS3VwfNBrKjwGsmCeFrIXoFZrabLzeaSJq1L58KzwIXrTIPqimuCnP5+EXIOKwUhS74ie1CWttz01nEvoHGqGo5EC7K7UpX5hhhE+/UJSaNbg9AgMBAAECgYBBRYIcyWk8lZ+JfUZeZUkNhIFlaMV7ImffVkwhFPPKAUsuRAC5yJwe8yKnNyyPOL82PJIGi2jLWYQUB7i3hMFcQpDxmsfDqJk3zEQHNYhDGHuU57il7Cunn567C1HNUbxIHAuLwTB+fYIpE5TGipqitkbZrLyvk8UxEe5DqATzgQJBAM9jarYTemoIiU2sVO7Y6oDOGGLqTy8tdEG57ePZtR90/bSBXwcQjoZ+MuHPwG3ZMUd4cklLl3yiAS+hRJgkfTECQQCzkYLyXV2eT6SegT2NGqtv3PR0yUuadrs54V6/KRgAfkflBj+DzXYHJEuLV5JYTTHiP8WRp2xV/8/ZQPrhlvjNAkBn+wW28r8uyMbm3d/bvYCeQjcx6R74nYarqahf1Hkeo47M4QyfQyrivgWO+JYXvY0as4ZBv5fdknCby/TTf4ARAkEAmeA3tjkL4H2fM7TMaf5QqqtNUEau4s6b4h2ec3FjgAi20ytngiqu2a/gjKeeYMzF0nuTch1mWMu98Q4d7vLQgQJAYTTzuYRcZvCAM7axHr6r3GdIPwNzEunDKe1X1TKc2/GNC1ws43QYhblUSaoJqvJTnsClVT+SF0hPOzvKJNCLyg=='
    public_key='MIGfMA0GCSqGSIb3DQEBAQUAA4GNADCBiQKBgQCReGUBlI3rnmSGmOfh4BAK+5Xgbz/P37Xphfnmjc5eT0Re6398CHqAu8dUMzjwUt1cHzQayo8BrJgnhayF6BWa2my83mkiatS+fCs8CF60yD6oprgpz+fhFyDisFIUu+IntQlrbc9NZxL6BxqhqORAuyu1KV+YYYRPv1CUmjW4PQIDAQAB'
    myencry=myencry(public_key)
    miwen=myencry.get_encry_str('hello')
    print miwen
    mydecry=mydecry(private_key)
    mingwen=mydecry.get_decry_str(miwen)
    print mingwen