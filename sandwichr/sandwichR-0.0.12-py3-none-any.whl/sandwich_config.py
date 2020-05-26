#!/usr/bin/env python3
import os.path
import json

class PinData():
  pinNumber = 0
  mode = 0
  request = 0
  moduleCount = 0
  minPulse = 0
  maxPulse = 0

class FloorIrCallbackData():
  floor_ir_1 = 0
  floor_ir_2 = 0
  floor_ir_3 = 0
  floor_ir_4 = 0
  floor_ir_5 = 0

class FrontIrCallbackData():
  front_ir_1 = 0
  front_ir_2 = 0

class SonarCallbackData():
  distance = 0

class EventCallbackData(FloorIrCallbackData, FrontIrCallbackData, SonarCallbackData):
  def __init__(self):
    floor_ir_1 = 0
    floor_ir_2 = 0
    floor_ir_3 = 0
    floor_ir_4 = 0
    floor_ir_5 = 0
    front_ir_1 = 0
    front_ir_2 = 0
    distance = 0

class Sandwich_Config():

  def readConfigFile(self, config_path, pins):
    if config_path.isspace():
      print("Pin configuration error : Empty dir")
      return

    if not os.path.isdir(config_path):
      print("Pin configuration error : Not dir")
      return

    if not os.path.isfile(config_path + "/pins.config"):
      print("Pin configuration error : config file not exist")
      retur

    self.jsonParser(config_path, pins)

  def jsonParser(self, config_path, pins):
    f = open(config_path + "/pins.config", 'r')
    configDatas = json.loads(f.read())
    # configDatas = rapidjson.loads(f.read())
    pindatas = configDatas.get('pins')

    if pindatas is None:
      print("Pin configuration error : file error")
      return

    for data in pindatas:
      pin = PinData()
      
      pinnum = data.get('number')
      if pinnum is None:
        print("Pin configuration error : file syntax error")
        return
      pin.pinNumber = pinnum
      
      mode = data.get('mode')
      if mode is None:
        print("Pin configuration error : file syntax error")
        return
      pin.mode = mode

      pin.moduleCount = data.get('moduleCount')
      pin.minPulse = data.get('minPulse')
      pin.maxPulse = data.get('maxPulse')

      pins[pinnum] = pin

  def __init__(self):
    pass

# if __name__ == '__main__':
#   pins = dict()
#   sc = Sandwich_Config()
#   sc.readConfigFile('../pins', pins)

#   for num, data in pins.items():
#     print( num, data.mode )
