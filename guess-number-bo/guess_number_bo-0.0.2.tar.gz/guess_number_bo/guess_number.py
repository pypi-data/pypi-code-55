import random
from enum import Enum, auto


class Result(Enum):
    BINGO = auto()
    HIGH = auto()
    LOW = auto()


class GuessNumber:
    """The class randomly chooses an integer 
    and then tells a human player if a guess is higher or lower than the number
    """

    def __init__(self):
        """ 
        Attributes:
            _low: low threshold for the random number
            _high: high threshold for the random number
            _player_cnt: number of players
            _target: a random number between (_low, _high)
        """
        self._low = 1
        self._high = 100
        self._player_cnt = 2
        self._target = random.randint(self._low, self._high)

    def guess(self, number: int) -> Result:
        """ Perform one guess

        Args:
            number: the number guessed

        Returns:
            Result.BINGO  if number == _target
            Result.HIGH   if number > _target
            Result.LOW    if number < _target
        """
        if number == self._target:
            return Result.BINGO

        if number > self._target:
            self._high = number if number < self._high else self._high
            return Result.HIGH
        else:
            self._low = number if number > self._low else self._low
            return Result.LOW

    def play(self) -> None:
        """ Play a game """
        print("Welcome to guessing number game!")

        customize = input(
            '''The default game is for 2 players. \
            Do you want to customize your game? [N/y]''')

        if customize != '' and customize.upper() == 'Y':
            while True:
                try:
                    player_cnt = input("Enter number of players: ")
                    self._player_cnt = int(player_cnt)
                    break
                except ValueError:
                    print("No valid integer! Please try again ...")

            while True:
                try:
                    low = input("Enter the smallest possible value: ")
                    self._low = int(low)
                    break
                except ValueError:
                    print("No valid integer! Please try again ...")

            while True:
                try:
                    high = input("Enter the largest possible value: ")
                    self._high = int(high)
                    break
                except ValueError:
                    print("No valid integer! Please try again ...")

            self._target = random.randint(self._low, self._high)

        playerID = 0
        while True:
            playerID = playerID % self._player_cnt
            print(f'Player {playerID + 1}\'s turn:')

            while True:
                try:
                    number = int(input(f'Please guess a number between {self._low} and {self._high}: '))
                    break
                except ValueError:
                    print("No valid integer! Please try again ...")

            result = self.guess(number)

            if result == Result.BINGO:
                print(f'Player {playerID + 1} wins! The number is {self._target}')
                return
            elif result == Result.HIGH:
                print(f'Too large!')
            elif result == Result.LOW:
                print(f'Too small!')

            playerID += 1

    def __repr__(self) -> str:
        """ Magic method (override for print) """
        pass
