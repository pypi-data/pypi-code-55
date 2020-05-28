import sys
import time
from pinpong.pinpong import *
from pinpong.libs.DFRobot_BUZZER import *

BUZZER_PIN = 7

board = PinPong("uno","com4")
board.connect()
buzzer = DFRobot_BUZZER(board, BUZZER_PIN)

while True:
  buzzer.on()
  time.sleep(1)
  buzzer.off()
  time.sleep(1)
