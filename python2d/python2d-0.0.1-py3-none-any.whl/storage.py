import json
import sys

def getpos(l, st):
    for i in range(len(st)):
        if st[i] == l:
            return i
    return -1

class database():
    def __init__(self, path, default={}, encryption=None, full=False):
        if full:
            self.path = path
        else:
            self.path = sys.path[0] + "/" + path
        self.encryption = encryption
        self.default = json.dumps(default, indent=0, sort_keys=True)
    
    def load(self):
        try:
            with open(self.path, "r") as f:
                data = f.read()
                if self.encryption:
                    return json.loads(self.decode(data))
                return json.loads(data)
        except:
            with open(self.path, "w") as f:
                if self.encryption:
                    f.write(self.encode(self.default))
                else:
                    f.write(self.default)
            return json.loads(self.default)
    
    def save(self, data):
        with open(self.path, "w") as file:
            if self.encryption:
                file.write(self.encode(json.dumps(data, indent=0, sort_keys=True)))
            else:
                file.write(json.dumps(data, indent=0, sort_keys=True))
    
    def encode(self, text):
        chars = "\n abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789@#€_&-+()/*\"':;!?,.~`|•√π÷×¶∆£¥$¢^°={}\\%©®™✓[]"
        for l in self.encryption:
            i = getpos(l, chars)
            nchars = l
            for p in range(len(chars)):
                if p == i:
                    continue
                nchars += chars[p]
            chars = nchars
        result = ""
        for l in text:
            i = getpos(l, chars)
            i += 37
            result += chars[i%len(chars)]
        return result
    
    def decode(self, text):
        chars = "\n abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789@#€_&-+()/*\"':;!?,.~`|•√π÷×¶∆£¥$¢^°={}\\%©®™✓[]"
        for l in self.encryption:
            i = getpos(l, chars)
            nchars = l
            for p in range(len(chars)):
                if p == i:
                    continue
                nchars += chars[p]
            chars = nchars
        result = ""
        for l in text:
            i = getpos(l, chars)
            i -= 37
            if i < 0:
                i += len(chars)
            result += chars[i]
        return result
