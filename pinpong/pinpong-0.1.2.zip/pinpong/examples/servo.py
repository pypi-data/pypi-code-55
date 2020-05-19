import sys
import time
from pinpong.pinpong import *

board = PinPong("uno","com4")
board.connect()

try:
  board.pin_mode(4,SERVO)
  while True:
    board.servo_write_angle(4,0)
    time.sleep(1)

    board.servo_write_angle(4,90)
    time.sleep(1)

    board.servo_write_angle(4,180)
    time.sleep(1)

    board.servo_write_angle(4,90)
    time.sleep(1)

except KeyboardInterrupt:
    board.shutdown()
    sys.exit(0)
