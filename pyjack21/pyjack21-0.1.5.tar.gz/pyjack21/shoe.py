from enum import Enum
import random


class Suit(Enum):
    heart = 1
    spade = 2
    club = 3
    diamond = 4

class Rank(Enum):
    ace = 1
    two = 2
    three = 3
    four = 4
    five = 5
    six = 6
    seven = 7
    eight = 8
    nine = 9
    ten = 10
    jack = 11
    queen = 12
    king = 13

class Card:
    def __init__(self, suit: Suit, rank: Rank):
        self.suit = suit
        self.rank = rank

    def get_suit(self):
        return self.suit

    def get_rank(self):
        return self.rank

    def char_rep(self):
        if self.rank == Rank.ace:
            return "A"
        elif self.rank == Rank.two:
            return "2"
        elif self.rank == Rank.three:
            return "3"
        elif self.rank == Rank.four:
            return "4"
        elif self.rank == Rank.five:
            return "5"
        elif self.rank == Rank.six:
            return "6"
        elif self.rank == Rank.seven:
            return "7"
        elif self.rank == Rank.eight:
            return "8"
        elif self.rank == Rank.nine:
            return "9"
        elif self.rank == Rank.ten:
            return "T"
        elif self.rank == Rank.jack:
            return "J"
        elif self.rank == Rank.queen:
            return "Q"
        elif self.rank == Rank.king:
            return "K"    
        else:
            return "?"

    def value(self, aces_high=True):
        if self.rank == Rank.ace:
            if aces_high:
                return 11
            else:
                return 1
        elif self.rank == Rank.two:
            return 2
        elif self.rank == Rank.three:
            return 3
        elif self.rank == Rank.four:
            return 4
        elif self.rank == Rank.five:
            return 5
        elif self.rank == Rank.six:
            return 6
        elif self.rank == Rank.seven:
            return 7
        elif self.rank == Rank.eight:
            return 8
        elif self.rank == Rank.nine:
            return 9
        elif self.rank == Rank.ten or self.rank == Rank.jack:
            return 10
        elif self.rank == Rank.queen or self.rank == Rank.king:
            return 10
        else:
            return -999

    def __cmp_value(self):
        if self.rank == Rank.ace:
            return 1
        elif self.rank == Rank.two:
            return 2
        elif self.rank == Rank.three:
            return 3
        elif self.rank == Rank.four:
            return 4
        elif self.rank == Rank.five:
            return 5
        elif self.rank == Rank.six:
            return 6
        elif self.rank == Rank.seven:
            return 7
        elif self.rank == Rank.eight:
            return 8
        elif self.rank == Rank.nine:
            return 9
        elif self.rank == Rank.ten:
            return 10
        elif self.rank == Rank.jack:
            return 11
        elif self.rank == Rank.queen:
            return 12
        elif self.rank == Rank.king:
            return 13    
        else:
            return 99

    def __cmp__(self, other):
        return cmp(self.__cmp_value(), other.__cmp_value())

    def __lt__(self, other):
        return self.__cmp_value() < other.__cmp_value()

    def __le__(self, other):
        return self.__cmp_value() <= other.__cmp_value()
    
    def __eq__(self, other):
        return self.__cmp_value() == other.__cmp_value()
    
    def __ne__(self, other):
        return self.__cmp_value() != other.__cmp_value()
    
    def __ge__(self, other):
        return self.__cmp_value() >= other.__cmp_value()
    
    def __gt__(self, other):
        return self.__cmp_value() >= other.__cmp_value()
    
    def __str__(self):
        return f'{self.suit} {self.rank}'


class Shoe:
    def __init__(self, deck_count: int):
        self.cards = self.__get_cards(deck_count)
        self.deck_count = deck_count
        self.discard_shown = []
        self.discard_hidden = []

    def deal(self):
        card = self.cards.pop(0)
        self.discard_shown.append(card)
        return card

    def burn(self):
        card = self.cards.pop(0)
        self.discard_hidden.append(card)

    def shuffle(self):
        random.shuffle(self.cards)

    def cards_left(self):
        return len(self.cards)


    def __get_cards(self, deck_count):
        cards = []
        for i in range(deck_count):
            for suit in Suit:
                for rank in Rank:
                    cards.append(Card(suit, rank))
        return cards

    def __str__(self):
        s = ""
        s += f'cards left: {self.cards_left()   }'
        # for card in self.cards:
           #  s += f'{card}'
        return s

if __name__ == "__main__":

    ace_hearts = Card(suit=Suit.heart, rank=Rank.ace)
    # print(f'This is the card: {ace_hearts}')

    shoe = Shoe(2)
    shoe.shuffle()
    # # print(f'{shoe}')
    shoe.burn()
    # print(f'{shoe.deal()}')
    # print(f'{shoe.deal()}')
    # print(f'{shoe.deal()}')
    # print(f'{shoe.deal().char_rep()}')
    # print(f'{shoe}')


    hand = []
    
    
    
    for i in range(7):
        hand.append(shoe.deal())
    
    s = ""
    for card in hand:
        s += f'{card} |'
    # print(s)
    
    hand = sorted(hand)

    s = ""
    for card in hand:
        s += f'{card} |'
    # print(s)
