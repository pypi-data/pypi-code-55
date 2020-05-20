import sys
import time
from pinpong.pinpong import *

BUTTON_PIN = 8

board = PinPong("uno","com4")
board.connect()

board.pin_mode(BUTTON_PIN, INPUT)
board.pin_mode(13, OUTPUT)
while True:
  v = board.read_digital(BUTTON_PIN)
  board.write_digital(13, v)
  time.sleep(0.1)
