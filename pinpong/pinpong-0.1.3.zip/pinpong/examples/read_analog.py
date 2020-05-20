import sys
import time
from pinpong.pinpong import *

ANALOG_PIN="A0"

board = PinPong("uno","com4")
board.connect()

board.pin_mode(ANALOG_PIN, ANALOG)
while True:
  v=board.read_analog(ANALOG_PIN)
  print("v=%d"%v)
  time.sleep(1)