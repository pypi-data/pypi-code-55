from Tic_Tac_Toe.Game_board import Board


class Game_Rule(Board):
    def __init__(self):
        Board.__init__(self)

    def isWin(self):
        board = self.getBoard()

        if board['1'] == board['2'] == board['3'] != ' ':
            return True
        elif board['4'] == board['5'] == board['6'] != ' ':
            return True
        elif board['7'] == board['8'] == board['9'] != ' ':
            return True
        elif board['7'] == board['1'] == board['4'] != ' ':
            return True
        elif board['2'] == board['8'] == board['5'] != ' ':
            return True
        elif board['3'] == board['6'] == board['9'] != ' ':
            return True
        elif board['7'] == board['3'] == board['5'] != ' ':
            return True
        elif board['1'] == board['5'] == board['9'] != ' ':
            return True
        else:
            return False
