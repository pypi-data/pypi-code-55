import random
import string
from typing import List

from .card import BriscolaCard, Card
from .interactive import InteractiveBriscola


class Player():

    number: int = 0

    @staticmethod
    def numberPlayer() -> int:
        Player.number += 1
        return Player.number - 1

    @staticmethod
    def resetNumber() -> None:
        Player.number = 0

    def __init__(self, name: str = ''):
        self.hand: List[Card] = []
        self.score: int = 0
        self.name: str = name
        self.number: int = Player.numberPlayer()
        if name == "":
            self.name = ''.join(random.choice(string.ascii_lowercase)
                                for i in range(3))
        self.name += ' ' + str(self.number)
        self.winnedcards: List[Card] = []
        self.chosencard: Card = None

    def drawcard(self, deck: List[Card]) -> str:
        drawed_card: Card = deck.pop(0)
        self.hand.append(drawed_card)
        return str(drawed_card)

    def playcard(self, game=None):
        self.chosencard = self.hand.pop(0)
        print("{name}\t({score}) played:\t{card}".format(name=self.name,
                                                         score=self.score,
                                                         card=self.chosencard))
        return self.chosencard

    def calculscore(self) -> None:
        self.score = sum((c.score for c in self.winnedcards))


class BriscolaPlayer(Player):

    def __init__(self, name: str, auto: bool = True):
        super().__init__(name)
        self.auto = auto
        # self.vector = BriscolaPlayerVector(self.number)

    def playcard(self, game=None) -> BriscolaCard:
        if not self.auto:
            InteractiveBriscola(self, game).cmdloop(
                intro='Your cards: ' + ', '.join(("{}: {}".format(i + 1, x)
                                                  for i, x in enumerate(
                                                  self.getstrhand()))))
        return super().playcard()

    def getstrhand(self) -> List[str]:
        return list(map(str, self.hand))


class ComputerBriscolaPlayer(Player):
    def __init__(self) -> None:
        super().__init__()
        self.name = "cmp_" + self.name
