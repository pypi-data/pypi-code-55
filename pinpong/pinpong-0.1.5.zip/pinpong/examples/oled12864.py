import sys
import time
from pinpong.pinpong import *
from pinpong.libs.DFRobot_SSD1306 import *

board = PinPong("uno","com4")
board.connect()
oled=SSD1306_I2C(128, 64, board)


while True:
  oled.fill(1)
  oled.show()
  time.sleep(1)
  
  oled.fill(0)
  oled.show()
  time.sleep(1)
  
  oled.text(0)
  oled.text("hello pinpong",8,8)
  oled.show()
  time.sleep(2)