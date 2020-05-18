import hmac
import hashlib
import time

class RollingTokenManager():

    class Token(object):
        def __init__(self, token, timestamp):
            self.token = token
            self.timestamp = timestamp
        
        def get_offset(self):
            return self.timestamp - current_timestamp()
    



    def __init__(self, secret, interval: int, tolerance = 1):
        self.secret = secret
        if type(self.secret) == str: self.secret = self.secret.encode('utf-8')
        self.interval = interval
        self.tolerance = tolerance
        self.active_tokens = []
    

    def current_timestamp(self) -> int:
        return int(time.time()) // self.interval

    def generate_token(self, offset = 0):
        timestamp = self.current_timestamp() + offset
        encoded_timestamp = str(timestamp).encode('utf-8')
        hmac_digest = hmac.new(self.secret, encoded_timestamp, hashlib.sha256)
        return RollingTokenManager.Token(hmac_digest.hexdigest(), timestamp)

    def refresh_tokens(self):
        for token in reversed(self.active_tokens):
            if abs(token.get_offset()) > self.tolerance: self.active_tokens.remove(token)
        
        if len(self.active_tokens) == 1+2*self.tolerance: return

        active_offsets = {t.get_offset() for t in self.active_tokens}

        for offset in range(-self.tolerance, self.tolerance+1):
            if offset in active_offsets: continue
            token = self.generate_token(offset=offset)
            self.active_tokens.append(token)


    def is_valid(self, token):
        self.refresh_tokens()

        for t in self.active_tokens:
            if t.token == token: return True
        return False
