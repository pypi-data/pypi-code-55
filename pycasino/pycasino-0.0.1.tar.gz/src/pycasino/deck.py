import collections
import enum
import itertools
import random


class Suit(enum.Enum):
    """Contains suits of the deck"""
    Clubs = '♣'
    Diamonds = '♦'
    Hearts = '♥'
    Spades = '♠'


class Value(enum.IntEnum):
    """Contains the values of the cards"""
    Ace = 1
    Two = 2
    Three = 3
    Four = 4
    Five = 5
    Six = 6
    Seven = 7
    Eight = 8
    Nine = 9
    Ten = 10
    Jack = 11
    Queen = 12
    King = 13


class Card:
    """Creates a playing card"""
    def __init__(self, suit=None, value=None):
        if value is None:
            self.suit, self.value = suit
        else:
            self.suit = suit
            self.value = value


class Deck(collections.deque):
    """Creates a deck of 52 playing cards"""
    def __init__(self):
        super().__init__(
            map(
                Card,
                itertools.product(
                    Suit.__members__.values(), Value.__members__.values()
                ),
            )
        )

    def shuffle(self) -> None:
        random.shuffle(self)

    deal = collections.deque.pop

    deal_from_bottom = collections.deque.popleft


collections.deck = Deck
