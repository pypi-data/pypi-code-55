# For running unit tests, use
# python -m unittest test

import unittest

from guess_number import GuessNumber, Result

class TestGuessNumber(unittest.TestCase):
    def setUp(self):
        self.gn = GuessNumber()
        self.target = self.gn._target

    def test_initialization(self): 
        self.assertEqual(self.gn._low, 1, 'incorrect low')
        self.assertEqual(self.gn._high, 100, 'incorrect high')
        self.assertEqual(self.gn._player_cnt, 2, 'incorrect player_cnt')
        self.assertEqual(self.gn._target, self.target, 'incorrect target')

    def test_guesslarge(self):
        self.assertEqual(self.gn.guess(self.target + 1), Result.HIGH, 'expect guess to be larger than target')

    def test_guesssmall(self):
        self.assertEqual(self.gn.guess(self.target - 1), Result.LOW, 'expect guess to be smaller than target')

    def test_guesssbingo(self):
        self.assertEqual(self.gn.guess(self.target), Result.BINGO, 'expect guess to be equal to target')
        
    
if __name__ == '__main__':
    unittest.main()