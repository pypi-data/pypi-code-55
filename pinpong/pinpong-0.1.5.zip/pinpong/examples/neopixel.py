import time
from pinpong.pinpong import *
from pinpong.libs.DFRobot_NEOPIXEL import *

NEOPIXEL_PIN = 7
PIXELS_NUM = 4

board = PinPong("leonardo","com5")
board.connect()
pixels = DFRobot_NEOPIXEL(NEOPIXEL_PIN)
pixels.begin(board, PIXELS_NUM)

while True:
  pixels.write(0, 0, 255 ,0)
  pixels.write(1, 255, 0, 0)
  pixels.write(2, 0, 0, 255)
  pixels.write(3, 255, 0, 255)
  time.sleep(1)
  pixels.write(1, 0, 255, 0)
  pixels.write(2, 255, 0, 0)
  pixels.write(3, 255, 255, 0)
  pixels.write(0, 0, 0, 255)
  time.sleep(1)