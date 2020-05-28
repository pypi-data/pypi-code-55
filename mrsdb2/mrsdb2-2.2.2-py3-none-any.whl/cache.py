import time
from multiprocessing import Process
import warnings
from mrsdb2.exceptions import *


class Cache:
    def __init__(self, *args, **kwargs):
        """
        Create cache
        """
        self.cache = kwargs.get('starting', {})
        self.expires = kwargs.get('expires', 60)
        self.expat = time.time()+self.expires
        self.maxlen = kwargs.get('max', 1028)
        self.hardexp = kwargs.get('hardexpires', 10)
        if kwargs.get('thread', True):
            self.loopthread = Process(target=self.loop, daemon=True)
            self.loopthread.start()
    

    def loop(self):
        """
        Caching process loop
        """
        while 1:
            if time.time() > self.expat+self.hardexp:
                raise CachingError("Cache renewal overdue.")

    
            if len(self.cache) > self.maxlen or time.time() > self.expat:
                self.renew()


    def renew(self):
        """
        Renew cache
        """
        self.cache = {}
        self.expat = time.time()+self.expires


    def add(self, key, value):
        """
        Add to cache
        """
        self.cache[key] = value