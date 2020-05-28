import sys
import time
from pinpong.pinpong import *
from pinpong.libs.DFRobot_DHT import *

DHT11_PIN = 6
DHT22_PIN = 7

board = PinPong("uno","com4")
board.connect()
dht = DFRobot_DHT(board)
dht.begin(DHT11_PIN, type=11)
dht.begin(DHT22_PIN, type=22)

while True:
  v = dht.read(DHT11_PIN)
  print("dht11 ",v)
  v = dht.read(DHT22_PIN)
  print("dht22 ",v)
  
  #print("distance = %d cm"%dis)
  time.sleep(1)


