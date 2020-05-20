import base64

def b64e (n):
    size = max((n.bit_length() + 7) // 8, 1)
    return base64.urlsafe_b64encode(n.to_bytes(size, 'big')).decode()

def b64d (t):
    return int.from_bytes(base64.urlsafe_b64decode(t), 'big')

def valid_b64 (s):
    try:
        base64.urlsafe_b64decode(s)
        return True
    except:
        return False
