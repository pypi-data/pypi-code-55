import sys
import time
from pinpong.pinpong import *

board = PinPong("uno","com4")
board.connect()

try:
  board.pin_mode(6, PWM)
  while True:
    for i in range(255):
      print(i)
      board.write_analog(6,i)
      time.sleep(0.05)
except KeyboardInterrupt:
    board.shutdown()
    sys.exit(0)
