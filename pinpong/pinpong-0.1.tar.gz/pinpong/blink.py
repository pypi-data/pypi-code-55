import sys
import time
from pinpong import *
from DFRobot_SSD1306 import *

def blink(board):
  ssd1306=SSD1306_I2C(128, 64, board)
  while True:
    '''
    my_board.i2c_write(4, [10]+[ord(x) for x in list("ON")])
    time.sleep(0.1)
    ret = my_board.i2c_read(4, 10, 2, None)
    print(ret)
    time.sleep(1)

    my_board.i2c_write(4, [10]+[ord(x) for x in list("OFF")])
    time.sleep(0.1)
    ret = my_board.i2c_read(4, 10, 2, None)
    print(ret)
    time.sleep(1)
    '''
    ssd1306.fill(1)
    ssd1306.show()
    time.sleep(1)
    
    ssd1306.fill(0)
    ssd1306.show()
    time.sleep(1)
    
    ssd1306.text(0)
    ssd1306.text("hello pinpong",8,8)
    ssd1306.show()
    time.sleep(2)
board = PinPong("uno","com4")
board.connect()

try:
    blink(board)
except KeyboardInterrupt:
    board.shutdown()
    sys.exit(0)
