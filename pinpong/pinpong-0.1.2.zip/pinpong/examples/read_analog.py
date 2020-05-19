import sys
import time
from pinpong.pinpong import *

board = PinPong("uno","com4")
board.connect()

try:
  board.pin_mode("A0", ANALOG)
  while True:
    v=board.read_analog("A0")
    print("v=%d"%v)
    time.sleep(1)
except KeyboardInterrupt:
    board.shutdown()
    sys.exit(0)
