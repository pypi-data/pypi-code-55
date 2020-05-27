import time
from pinpong.pinpong import *

class DFRobot_DHT:
  def __init__(self,board):
    self.board = board

  def begin(self, pin, type):
    self.pin = pin
    self.type = type
    self.board.board.set_pin_mode_dht(self.pin, self.type, differential=.01)

  def read(self):
    return self.board.board.dht_read(self.pin)