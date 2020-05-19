import sys
import time
from pinpong.pinpong import *
from pinpong.libs.DFRobot_HCSR04 import *

TRIGER_PIN = 7
ECHO_PIN = 8

board = PinPong("uno","com4")
board.connect()
sonar = DFRobot_HCSR04(board)
sonar.begin(TRIGER_PIN, ECHO_PIN)

try:
  while True:
    dis = sonar.read()
    print("distance = %d cm"%dis)
    time.sleep(0.1)
except KeyboardInterrupt:
    board.shutdown()
    sys.exit(0)


