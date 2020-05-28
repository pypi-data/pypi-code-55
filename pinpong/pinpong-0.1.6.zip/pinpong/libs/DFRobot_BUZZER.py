import time
from pinpong.pinpong import *

class DFRobot_BUZZER:
  def __init__(self, board, pin):
    self.pin  = pin
    self.board = board
    self.board.board.set_pin_mode_tone(self.pin)

  def on(self):
    self.board.board.play_tone(self.pin, 1000, 0)

  def off(self):
    self.board.board.play_tone(self.pin, 0, 0)
