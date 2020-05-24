import time
from multiprocessing import Process
import warnings


class Cache:
    def __init__(self, *args, **kwargs):
        self.cache = kwargs.get('starting', {})
        self.expires = kwargs.get('expires', 60)
        self.expat = time.time()+self.expires
        self.maxlen = kwargs.get('max', 1028)
        self.hardexp = kwargs.get('hardexpires', 10)
        if kwargs.get('thread', True):
            self.loopthread = Process(target=self.loop, daemon=True)
            self.loopthread.start()
    

    def loop(self):
        while 1:
            if time.time() > self.expat+self.hardexp:
                warnings.warn("Cache renewal overdue.", category=UserWarning)

    
            if len(self.cache) > self.maxlen or time.time() > self.expat:
                self.renew()


    def renew(self):
        self.cache = {}
        self.expat = time.time()+self.expires


    def add(self, key, value):
        self.cache[key] = value