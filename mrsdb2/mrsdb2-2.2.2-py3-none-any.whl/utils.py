import pickle
import binascii
import bcrypt
import re
import requests
import hashlib
import uuid


class Model:
    def Required(exception=KeyError):
        return ('$MDLREQ', exception)


    def _ru(kind):
        """
        Do not call.
        """
        if kind.lower() == 'int':
            return uuid.uuid4().int
        elif kind.lower() == 'hex':
            return uuid.uuid4().hex
        elif kind.lower() == 'bytes':
            return uuid.uuid4().bytes
        elif kind.lower() == 'node':
            return uuid.uuid4().node
        elif kind.upper() == 'UUID':
            return uuid.uuid4()
        raise ValueError(f'unknown type "{kind}"')


    def RandomUnique(kind='hex'):
        return ('$MDLRUQ', Model._ru, kind)
        

def Pickle(obj, legacy=False, *args, **kwargs):
    """
    Make a (pickleable) Python object database writable.
    """
    p = binascii.hexlify(pickle.dumps(obj, *args, **kwargs)).decode("utf-8")
    if legacy:
        raise RuntimeError('Legacy mode is not supported.')
    else:
        return ('$PYCKLE', p)


def BigInt(i, legacy=False):
    """
    Make an integer over 64 (or 32) bits database writable.
    """
    if i.bit_length() >= 64:
        if legacy:
            raise RuntimeError('Legacy mode is not supported.')
        else:
            return ('BIGINT', str(i))
    else:
        return i


def BigFloat(i, legacy=False):
    """
    Make a float over 64 bits database writable.
    """
    if i.bit_length() >= 64:
        if legacy:
            raise RuntimeError('Legacy mode is not supported.')
        else:
            return ('BIGFLT', str(i))
    else:
        return i


class Security:
    def make_hash(plain, rounds=8):
        """
        Make a secure bcrypt hash.
        Check it with Security.check_password().
        """
        passwd = plain
        if type(plain) == str:
            passwd = plain.encode()
        return bcrypt.hashpw(passwd, bcrypt.gensalt(rounds=rounds))


    def check_password(plain, hashed):
        """
        Check a bcrypt hash.
        Make one with Security.make_hash().
        """
        passwd = plain
        if type(plain) == str:
            passwd = plain.encode()
        return bcrypt.checkpw(passwd, hashed)


    def password_score(plain, checkforpwn=True):
        """
        Create a password score
        Returns score (int 0-10), positives (list), negatives (list).
        """
        # Decode bytes password.
        if type(plain) == bytes:
            plain = plain.decode()

        
        password = plain
        positives = []
        negatives = []
        score = 0
        

        # Check for length greater than 6.
        if len(password) < 6:
            negatives.append('Length')
        else:
            score += 3.5
            positives.append('Length')
        
        
        # Check for symbols/special chars.
        if not re.compile('[^0-9a-zA-Z]+').search(password):
            negatives.append('Symbols')
        else:
            score += 3.5
            positives.append('Symbols')

        
        # Check for password pwn/leak.
        if checkforpwn:
            pwa = hashlib.sha1(password.encode()).hexdigest()
            pw5 = pwa[:5]
            pws = pwa[5:]
            r = requests.get(f'https://api.pwnedpasswords.com/range/{pw5}')
            rt = r.text
            r.raise_for_status()
            il = False
            for l in rt.split('\n'):
                if len(l.split(':')) == 2:
                    if l.split(':')[0] == pws.upper():
                        negatives.append('Leaked')
                        score = 0
                        il = True
            if not il:
                score += 3
        else:
            score += 3


        # Dont allow score greater than 10.
        if score > 10:
            score = 10
        

        return score, positives, negatives


