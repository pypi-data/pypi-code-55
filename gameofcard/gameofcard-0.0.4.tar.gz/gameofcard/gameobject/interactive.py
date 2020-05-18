import cmd


class Interactive(cmd.Cmd):
    """docstring for ."""

    def __init__(self):
        super().__init__()


class InteractiveBriscola(Interactive):
    completekey = 'tab'

    def __init__(self, actual_player, game):
        super().__init__()
        self.player = actual_player
        self.cards = self.player.getstrhand()
        self.cardsdisplay = ', '.join(
            ["{}: {}".format(i + 1, c) for i, c in enumerate(self.cards)])
        self.game = game
        InteractiveBriscola.prompt = actual_player.name + ' >'

    def do_trump(self):
        """Display the trump card."""
        print("The trump card is {}\n".format(str(self.game.trumpcard)))

    def do_card(self, arg):
        """Display player's cards separate with a comma."""
        print(self.cardsdisplay)

    def do_play(self, arg=0):
        """play [cardname|numcard]\nPick up a card to play."""
        if arg.replace(' ', ' ') in self.cards or (
                arg.isdigit() and 0 < int(arg) <= len(self.cards)):
            indchosen = self.cards.index(
                arg) if not arg.isdigit() else int(arg) - 1
            self.player.hand[0], self.player.hand[
                indchosen] = self.player.hand[indchosen], self.player.hand[0]
            return True
        else:
            print("Please chose a card in your hand.\n", self.cardsdisplay)

    def complete_play(self, text, line, begidx, endidx):
        if text:
            return [f for f in self.cards if f.startswith(text)]
        return self.cards

    def do_exit(self, line):
        """Exit the game (Your progression will be lost)."""
        exit()
        return True
