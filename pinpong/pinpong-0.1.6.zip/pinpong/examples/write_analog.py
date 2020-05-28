import sys
import time
from pinpong.pinpong import *

PWM_PIN = 6

board = PinPong("uno","com4")
board.connect()


board.pin_mode(PWM_PIN, PWM)
while True:
  for i in range(255):
    print(i)
    board.write_analog(PWM_PIN,i)
    time.sleep(0.05)
