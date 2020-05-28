"""implement a data store with garbage collection.
"""
import random
import time

__version__="5.1" #VERSION#

def _inttime():
    return int(time.time())

# pylint: disable= invalid-name

_max_rand= 2**32-1

def rand_key():
    """return a 8-character random hex-string."""
    return "%08x" % random.randint(0,_max_rand)

class Store():
    """Implements a data store with garbage collection.

    This class implements a data store where data items are referenced by
    string keys that are generated with a random generator function. After a
    time that can be specified at class instantiation, elements of the store
    that were not acessed for this time are removed.
    """
    def __init__(self, hold_time= 600):
        self._hold_time= hold_time
        self._dict= {}
    def _new_key(self):
        """generate a new key not already in the store."""
        while True:
            key= rand_key()
            if key not in self._dict:
                break
        return key
    def _garbage_collector(self):
        now= _inttime()
        del_lst= []
        for (k,v) in self._dict.items():
            if v[0] is None:
                continue
            if now-v[0] > self._hold_time:
                del_lst.append(k)
        for k in del_lst:
            del self._dict[k]
    def new(self, user_key=None, keep_forever= False):
        """put new element in the store."""
        self._garbage_collector()
        if user_key is None:
            k= self._new_key()
        else:
            k= user_key
        if not keep_forever:
            time_= _inttime()
        else:
            time_= None
        self._dict[k]= [time_,None]
        return k
    def set(self,key,val):
        """change or set an element in the store."""
        elm= self._dict[key]
        elm[0]= _inttime()
        elm[1]= val
    def get(self,key):
        """get an element from the store."""
        elm= self._dict[key]
        elm[0]= _inttime()
        return elm[1]
    def delete(self,key):
        """delete an element in the store."""
        del self._dict[key]
