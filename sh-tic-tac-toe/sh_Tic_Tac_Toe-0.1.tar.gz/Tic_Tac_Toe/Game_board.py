class Board(object):
    def __init__(self):
        self.board = None

    def createBoard(self):
        board = {'1': ' ', '2': ' ', '3': ' ',
                 '4': ' ', '5': ' ', '6': ' ',
                 '7': ' ', '8': ' ', '9': ' '}
        self.board = board
        return self.board

    def getBoard(self):
        return self.board

    def showBoard(self):
        print(self.board['1'] + ' | ' + self.board['2'] + ' | ' + self.board['3'])
        print('- + - + -')
        print(self.board['4'] + ' | ' + self.board['5'] + ' | ' + self.board['6'])
        print('- + - + -')
        print(self.board['7'] + ' | ' + self.board['8'] + ' | ' + self.board['9'])

    def showNumberinBoard(self):
        board = {'1': '1', '2': '2', '3': '3',
                 '4': '4', '5': '5', '6': '6',
                 '7': '7', '8': '8', '9': '9'}
        print(board['1'] + ' | ' + board['2'] + ' | ' + board['3'])
        print('- + - + -')
        print(board['4'] + ' | ' + board['5'] + ' | ' + board['6'])
        print('- + - + -')
        print(board['7'] + ' | ' + board['8'] + ' | ' + board['9'])

