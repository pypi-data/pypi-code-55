import sys
import time
from pinpong.pinpong import *

board = PinPong("uno","com4")
board.connect()

try:
  board.pin_mode(13, OUTPUT)
  while True:
    board.write_digital(13, 0)
    time.sleep(1)

    board.write_digital(13, 90)
    time.sleep(1)

except KeyboardInterrupt:
    board.shutdown()
    sys.exit(0)
