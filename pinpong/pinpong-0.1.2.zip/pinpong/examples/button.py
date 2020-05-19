import sys
import time
from pinpong.pinpong import *

board = PinPong("uno","com4")
board.connect()

try:
  board.pin_mode(8, INPUT)
  board.pin_mode(13, OUTPUT)
  while True:
    v = board.read_digital(8)
    board.write_digital(13, v)
    time.sleep(0.1)

except KeyboardInterrupt:
    board.shutdown()
    sys.exit(0)
