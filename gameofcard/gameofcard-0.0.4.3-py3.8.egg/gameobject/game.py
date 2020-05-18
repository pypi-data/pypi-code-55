from typing import List

from .card import BriscolaCard
from .deck import BriscolaDeck
from .player import BriscolaPlayer, Player


class Game():
    def __init__(self) -> None:
        pass


class BriscolaGame(Game):

    def __init__(self, players: List[BriscolaPlayer]):
        self.deckobject = BriscolaDeck()
        self.players = players
        self.lenplayers = len(players)
        self.trumpcard = self.deckobject.deck[-1]
        print("The trump card is {}\n".format(str(self.trumpcard)))
        self.trump = self.trumpcard.color
        BriscolaDeck.reorder(self.trump)
        self.startgame()
        self.playaparty()

    def startgame(self) -> None:
        for _ in range(3):
            self.alldraw()
        # store state

    def calculate_whowin(self, cardplayed: List[BriscolaCard]) -> int:
        indbestcard = 0
        asked = cardplayed[0]
        for i, c in enumerate(cardplayed):
            if c.color == self.trump:
                if asked.color != self.trump or c.gamevalue >= asked.gamevalue:
                    asked = c
            if asked.color == c.color and c.gamevalue >= asked.gamevalue:
                indbestcard = i
                asked = c
        return indbestcard

    def playoneturn(self) -> None:
        cardplayed = []
        for p in self.players:
            # store state
            cardplayed.append(p.playcard(self))
        whowin = self.calculate_whowin(cardplayed)
        self.players[whowin].winnedcards.extend(cardplayed)
        print('{} win the turn!'.format(self.players[whowin].name))
        self.players = self.players[whowin:] + self.players[:whowin]

    def stoptheparty(self) -> bool:
        deck = self.deckobject.deck
        lendeck = len(deck)
        first_hand = self.players[0].hand
        if (lendeck == lendeck % self.lenplayers) and first_hand == []:
            Player.resetNumber()
            # store state
            if deck != []:
                self.players[0].winnedcards.append(deck.pop(0))
                self.players[0].calculscore()
            return False
        else:
            return True

    def alldraw(self) -> None:
        for p in self.players:
            p.drawcard(self.deckobject.deck)

    def allscore(self) -> None:
        for p in self.players:
            p.calculscore()

    def printenscore(self) -> None:
        self.players.sort(key=lambda x: x.score, reverse=True)
        print("{} win with {}".format(
            self.players[0].name, self.players[0].score))
        print("\n".join(("{}\t{}".format(p.name, p.score)
                         for p in self.players[1:])))

    def playaparty(self) -> None:
        deck = self.deckobject.deck
        while self.stoptheparty():
            self.playoneturn()
            lendeck = len(deck)
            if (lendeck != lendeck % self.lenplayers):
                self.alldraw()
            self.allscore()
            print()
        self.printenscore()
