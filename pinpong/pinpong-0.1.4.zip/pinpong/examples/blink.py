import sys
import time
from pinpong.pinpong import *

LED_PIN = 13

board = PinPong("leonardo","com5")
board.connect()

board.pin_mode(LED_PIN, OUTPUT)
while True:
  board.write_digital(LED_PIN, 0)
  time.sleep(1)

  board.write_digital(LED_PIN, 90)
  time.sleep(1)
