import itertools
import random
from typing import List

from .card import Card, BriscolaCard


class Deck():
    def __init__(self, values: List[str],
                 colors: List[str], cardobject: type = Card) -> None:
        self.deck: List[Card] = [cardobject(v, c)
                                 for c, v in itertools.product(colors, values)]

    def shuffle(self) -> None:
        random.shuffle(self.deck)

    def __str__(self) -> str:
        return "\n".join((str(c) for c in self.deck))


class BriscolaDeck(Deck):
    colors = ['Gold', 'WoodenStick', 'Sword', 'Cup']
    values = (("As", 10, 11),
              ("3", 9, 10),
              ("King", 8, 4),
              ("Horseman", 7, 3),
              ("Jack", 6, 2),
              ("7", 5, 0),
              ("6", 4, 0),
              ("5", 3, 0),
              ("4", 2, 0),
              ("2", 1, 0))
    ordereddeck: List[BriscolaCard] = []

    def __init__(self) -> None:
        super().__init__(BriscolaDeck.values, BriscolaDeck.colors,
                         BriscolaCard)
        BriscolaDeck.ordereddeck = self.deck.copy()
        self.shuffle()

    @staticmethod
    def reorder(trump: str) -> None:
        bod = BriscolaDeck.ordereddeck
        lenVal = len(BriscolaDeck.values)
        start = BriscolaDeck.colors.index(trump) * lenVal
        end = start + lenVal
        bod[0: lenVal], bod[start: end] = bod[start: end], bod[0: lenVal]
