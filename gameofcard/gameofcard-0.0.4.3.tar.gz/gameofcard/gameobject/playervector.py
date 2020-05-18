from typing import List

from .deck import Deck, BriscolaDeck


class PlayerVector():
    def __init__(self, gameDeck: Deck, playernumber: int):
        self.playernumber = playernumber
        self.gameDeck = gameDeck
        self.cards: List[int] = []


class BriscolaPlayerVector(PlayerVector):
    def __init__(self, playernumber: int = 0) -> None:
        super().__init__(BriscolaDeck, playernumber)
        self.scores = []
        self.played = []
