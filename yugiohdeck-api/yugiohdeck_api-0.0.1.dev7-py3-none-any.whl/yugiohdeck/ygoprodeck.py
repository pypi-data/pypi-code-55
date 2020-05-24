import asyncio
import time
import itertools
import sqlite3
import json
import aiohttp
from sys import stderr
from random import randint
from .config import DEBUG
from .ygoprodeck_dbstructure import dbsetup

class RateLimit:
    PER_SECOND = 15
    MAX_TOKENS = 5
    # max burst = PER_SECOND + MAX_TOKENS
    
    def __init__(self):
        self.allowed = self.MAX_TOKENS
        self.init = time.monotonic()
        self.lastUpdate = self.init
        self.count = 0

    async def ask(self):
        if self.allowed < 1:
            for c in itertools.count():
                if self.tick():
                    break
                await asyncio.sleep(.05 * randint(0, 2**min(c,5) - 1))
        self.allowed -= 1
        self.count += 1
        
    def tick(self):
        now = time.monotonic()
        allowedNow = self.PER_SECOND * (now - self.lastUpdate)
        if allowedNow < 1:
            return False
        # print('TICK:\n.allowed: %f -> %f\n.lastUpdate: %f -> %f' % (self.allowed, min(allowedNow, self.MAX_TOKENS), self.lastUpdate, now))
        self.allowed = min(allowedNow, self.MAX_TOKENS)
        self.lastUpdate = now
        return True
        
    def report(self):
        DEBUG('We have sent %d requests over the last %f seconds.' % (self.count, time.monotonic()-self.init))
        
rate_limit = RateLimit()

cache_glob = None
EXPIRY = 2*24*60*60
async def Request(passcode):
    global cache_glob
    if cache_glob is None:
        db = sqlite3.connect('ygoprodeck-cache.sqlite')
        dbsetup(db)
        db.execute('''DELETE FROM data WHERE expiry < ?''', (time.time(),))
        cache = dict((key, value is not None and json.loads(value)[0] or None) for key,value in db.execute('''SELECT key,value FROM data'''))
        cache_glob = (db,cache)
    else:
        (db,cache) = cache_glob
    
    try:
        res = cache[passcode]
        if isinstance(res, asyncio.Event):
            DEBUG('YGOProDeck Cache wait: %d' % passcode)
            await res.wait()
            DEBUG('YGOProDeck Cache hit: %d' % passcode)
            return cache[passcode]
        else:
            DEBUG('YGOProDeck Cache hit: %d' % passcode)
            return res
    except KeyError:
        DEBUG('YGOProDeck Cache miss: %d' % passcode)
        pass
    
    e = asyncio.Event()
    cache[passcode] = e
    await rate_limit.ask()
    DEBUG('Asking for data: %d' % passcode)
    rate_limit.report()
    async with aiohttp.request(method='GET', url=('https://db.ygoprodeck.com/api/v6/cardinfo.php?id=%d&misc=yes' % passcode)) as r:
        try:
            if r.status == 429:
                print('Hit the YGOProDeck rate limit - try again in an hour, and don\'t run multiple processes in parallel.', file=stderr)
                cache[passcode] = None
                e.set()
                return None
            r.raise_for_status()
            data = await r.text()
        except aiohttp.ClientResponseError:
            data = None
        db.execute('''INSERT INTO data (key,value,expiry) VALUES (?,?,?)''', (passcode,data,time.time()+EXPIRY))
        db.commit()
        if data is not None:
            data = json.loads(data)
            try:
                data = data[0]
            except KeyError:
                data = None
        cache[passcode] = data
        e.set()
        DEBUG('Got data: %d' % passcode)
        return data
