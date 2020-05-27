import sys
import time
from pinpong.pinpong import *
from pinpong.libs.DFRobot_URM09 import *

board = PinPong("uno", "com4")
board.connect()


urm = DFRobot_URM09()
urm.begin(board,0x20)
urm.setModeRange(urm._MEASURE_MODE_AUTOMATIC ,urm._MEASURE_RANG_500)
while True:
  dist =urm.getDistance()
  temp = urm.getTemperature()

  print("Temperature is %.2f .c    "%temp)
  print("Distance is %d cm         "%dist)
  time.sleep(0.5)
