import sys
import time
from pinpong.pinpong import *
from pinpong.libs.DFRobot_DHT import *

DHT11_PIN = 7
#DHT22_PIN = 8

board = PinPong("uno","com4")
board.connect()
dht = DFRobot_DHT(board)
dht.begin(DHT11_PIN, type=11)

try:
  while True:
    v = dht.read()
    print(v)
    #print("distance = %d cm"%dis)
    time.sleep(1)
except KeyboardInterrupt:
    board.shutdown()
    sys.exit(0)


