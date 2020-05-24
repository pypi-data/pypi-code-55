from base64 import standard_b64encode, standard_b64decode
from urllib.parse import urljoin, urlparse, quote, unquote
from functools import reduce
from collections import namedtuple
import operator
import asyncio
import ygorganization
from . import ygoprodeck
from .config import DEBUG, SETTINGS

BITS_PER_CARD_CODE = 27
BITS_PER_CARD_COUNT = 2

Deck = namedtuple('Deck', ['name','decks'])
Decks = namedtuple('Decks', ['main','extra','side'])

async def ResolveCardData(card):
    card.ygoprodeckData = await ygoprodeck.Request(card.passcode)
    if card.ygoprodeckData is None:
        return
    try:
        konamiId = card.ygoprodeckData['misc_info'][0]['konami_id']
    except KeyError:
        return
    card.ygorgData = await ygorganization.GetCardData(konamiId)

class Card:
    passcode = None
    count = None
    ygoprodeckData = None
    ygorgData = None
    
    def __init__(self, passcode, count):
        self.passcode = passcode
        self.count = count
        
    def __repr__(self):
        return '%dx #%s [%s]' % (self.count, self.passcode, self.ygoprodeckData is None and '<no data>' or self.ygoprodeckData['name'])
        
    def __iter__(self):
        return iter((self.passcode, self.count))

def URLToFragment(url):
    base = urlparse(SETTINGS['baseURL'])
    url = urlparse(url)
    assert(base.netloc == url.netloc)
    return url.fragment
    
def EncodeDeck(cards):
    binary = ''.join((bin(passcode)[2:].rjust(BITS_PER_CARD_CODE,'0') + bin(count)[2:].rjust(BITS_PER_CARD_COUNT,'0')) for (passcode,count) in cards)
    length = len(binary)
    if length%8 > 0:
        binary += ('0'*(8-(length%8)))
    assert(len(binary)%8 == 0)
    return standard_b64encode(bytes(int(binary[base: base+8],2) for base in range(0,len(binary),8))).decode()
    
def DecodeDeck(str):
    binary = reduce(operator.add, map(lambda s: s[2:].rjust(8,'0'), map(bin, standard_b64decode(str))), '')
    
    bpcc = BITS_PER_CARD_CODE
    bpc = BITS_PER_CARD_CODE+BITS_PER_CARD_COUNT
    #assert((len(binary) % bpc) == 0)
    return [Card(
        passcode=int(binary[base : base+bpcc], 2),
        count=int(binary[base+bpcc : base+bpc], 2),
    ) for base in range(0,len(binary)-bpc+1, bpc)]
    
def DecodeFragment(fragment):
    parts = fragment.split(':')
    assert(1 <= len(parts) <= 2)
    
    deckParts = parts[0].split(';')
    assert(1 <= len(deckParts) <= 3)
    
    return Deck(
        name=(len(parts) > 1 and unquote(parts[1]) or None),
        decks=Decks(
            main=DecodeDeck(deckParts[0]),
            extra=(len(deckParts) > 1 and DecodeDeck(deckParts[1]) or []),
            side=(len(deckParts) > 2 and DecodeDeck(deckParts[2]) or [])
        )
    )

def ParseURLPasscodes(url):
    return DecodeFragment(URLToFragment(url))

def ResolveDeck(deck):
    return asyncio.gather(*(ResolveCardData(card) for card in deck))

async def ParseURLData(url):
    data = ParseURLPasscodes(url)
    await asyncio.gather(ResolveDeck(data.decks.main), ResolveDeck(data.decks.extra), ResolveDeck(data.decks.side))
    return data
    
def GetDeckURL(deck):
    (name, decks) = deck
    (main, extra, side) = decks
    
    fragment = '/#'
    fragment += EncodeDeck(main)
    if extra or side:
        fragment += ';'
        fragment += EncodeDeck(extra)
    if side:
        fragment += ';'
        fragment += EncodeDeck(side)
    fragment += ':'
    fragment += quote(name)
    return urljoin(SETTINGS['baseURL'], fragment)
