from Tic_Tac_Toe.Game_Rule import Game_Rule


class Game(Game_Rule):
    def __init__(self):

        Game_Rule.__init__(self)

        self.turn = None
        self.count = 0
        self.gameOver = False



    def changeTurn(self):
        if self.turn == 'X':
            self.turn = 'O'
        else:
            self.turn = 'X'

    def isEmpty(self, move):

        return self.board[move] == ' '

    def reset(self):
        reset = input("Do want to play Again?(y/n)")
        if reset == 'y' or reset == 'Y':
            self.createBoard()
            self.gameOver = False
            self.game()
        else:
            return



    def game(self):
        self.turn = 'X'

        self.showNumberinBoard()
        self.createBoard()
        print("Here is the game board: ")
        self.showBoard()

        while self.gameOver is False:
            print('Your turn: {} and move to which place? '.format(self.turn))

            move = input()

            if self.isEmpty(move):
                self.board[move] = self.turn
                self.count += 1
                self.showBoard()
            else:
                print('This place is already filled.')
                continue

            if self.count == 9:
                print('Tie! Game over!')
                self.gameOver = True

            if self.isWin() is True:
                print("The winner is {}. Game over!".format(self.turn))
                self.gameOver = True

            else:
                self.changeTurn()

        self.reset()





