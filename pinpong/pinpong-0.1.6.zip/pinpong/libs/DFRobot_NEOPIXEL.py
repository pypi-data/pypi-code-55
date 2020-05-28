import time
from pinpong.pinpong import *

class DFRobot_NEOPIXEL:
  def __init__(self, board, pin):
    self.pin  = pin
    self.board = board

  def begin(self, num):
    self.num = num
    self.board.pin_mode(self.pin, NEOPIXEL)
    self.board.board.neopixel_config(self.pin,self.num)
    time.sleep(0.1)

  def write(self , n, r, g, b):
    self.board.board.neopixel_write(n,(r,g,b))
