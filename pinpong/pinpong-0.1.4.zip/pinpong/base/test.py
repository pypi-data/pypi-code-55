# -*- coding: UTF-8 -*-

import time
from pinpong import *

#boardname可以是uno, handlepi,leonardo, mega2560
uno = PinPong(boardname="uno",port="com4")
uno.connect()
uno.pin_mode(13,OUTPUT)

leonardo = PinPong("leonardo","com5")
leonardo.connect()
leonardo.pin_mode(13,OUTPUT)

while True:
  uno.write_digital(13,1)
  leonardo.write_digital(13,1)
  time.sleep(1)
  
  uno.write_digital(13,0)
  leonardo.write_digital(13,0)
  time.sleep(1)
  