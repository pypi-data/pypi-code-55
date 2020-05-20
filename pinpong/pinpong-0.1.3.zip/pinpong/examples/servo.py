import sys
import time
from pinpong.pinpong import *

SERVO_PIN = 4

board = PinPong("uno","com4")
board.connect()


board.pin_mode(SERVO_PIN, SERVO)
while True:
  board.servo_write_angle(SERVO_PIN,0)
  time.sleep(1)

  board.servo_write_angle(SERVO_PIN,90)
  time.sleep(1)

  board.servo_write_angle(SERVO_PIN,180)
  time.sleep(1)

  board.servo_write_angle(SERVO_PIN,90)
  time.sleep(1)