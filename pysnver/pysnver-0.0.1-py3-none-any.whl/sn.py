from ctypes import *
import os
import platform

lib_path = os.path.join(
    os.path.dirname(os.path.realpath(__file__)),
    'so/libtokver.so'
)
c_sn_verifier = cdll.LoadLibrary(lib_path)

c_sn_verifier.c_verify_token.argtypes = [
    c_void_p
]
c_sn_verifier.c_verify_token.restype = c_bool


class SerialNum(object):

    @staticmethod
    def verify(tok: str):
        btok = tok.encode()
        c_tok = c_char_p(btok)
        val = c_sn_verifier.c_verify_token(c_tok)
        return val
