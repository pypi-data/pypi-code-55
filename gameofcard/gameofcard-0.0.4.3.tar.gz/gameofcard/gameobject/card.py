class Card():

    def __init__(self, value, color):
        self.color: str = color
        self.value: str = value

    def __str__(self):
        return "{v} of {c}".format(v=self.value, c=self.color)


class BriscolaCard(Card):
    def __init__(self, value: str, color: str):
        super().__init__(value, color)
        self.value, self.gamevalue, self.score = self.value
