
#!/usr/bin/env python3
import enum
import threading
import time
import serial
import queue
import random
import struct
import pkg_resources

from sandwichR.sandwich_config import *

MOTOR_LF = 0
MOTOR_LD = 1
MOTOR_RF = 2
MOTOR_RD = 3

MOTOR_L_F = 0
MOTOR_L_D = 0
MOTOR_R_F = 1
MOTOR_R_D = 1

OMNI_MOTOR_L = 0
OMNI_MOTOR_T = 1
OMNI_MOTOR_R = 2
OMNI_MOTOR_F = 0
OMNI_MOTOR_D = 1

LED_PIN        = 10
BUZZER_PIN     = 11
SONAR_PIN      = 12
FLOOR_IR_1_PIN = 15
FLOOR_IR_2_PIN = 16
FLOOR_IR_3_PIN = 17
FLOOR_IR_4_PIN = 20
FLOOR_IR_5_PIN = 21
# TODO : INSERT PROTOCOL
IMU_1_PIN      = 18
IMU_2_PIN      = 19
FRONT_IR_1_PIN = 13
FRONT_IR_2_PIN = 14

class Wheels(enum.Enum):
  NORMAL = 1
  OMNI = 2
  MECANUM = 3

class Events(enum.Enum):
  FLOOR_IR_EVENT = 1
  FRONT_IR_EVENT = 2
  SONAR_EVENT = 3
  IMU_EVENT = 4

class Sandwich_Baseboard():
  def __init__(self, wheelType, config_dir=None):
    self.pins = dict()
    self.eventHandlerDic = dict()
    self.serialBuf = queue.Queue()
    self.serialPort = None
    self.contorlBuf = queue.Queue()
    self.wheelType = wheelType

    #
    self.front_ir_1 = 0
    self.front_ir_2 = 0

    self.floor_ir_1 = 0
    self.floor_ir_2 = 0
    self.floor_ir_3 = 0
    self.floor_ir_4 = 0
    self.floor_ir_5 = 0

    self.sonar_1 = 0

    if config_dir == None:
      config_dir = pkg_resources.resource_filename(__package__,"pins")

    conf = Sandwich_Config()
    conf.readConfigFile(config_dir, self.pins)
  
  def boardInit(self):
    dataGetterTH = threading.Thread(target=self.dataGetter)
    dataGetterTH.daemon = True
    dataGetterTH.start()
    time.sleep(0.1)

    serialRecvTH = threading.Thread(target=self.serialReceiver)
    serialRecvTH.daemon = True
    serialRecvTH.start()
    time.sleep(0.1)

    serialParserTH = threading.Thread(target=self.serialParser)
    serialParserTH.daemon = True
    serialParserTH.start()
    time.sleep(0.1)

    dataSenderTH = threading.Thread(target=self.dataSender)
    dataSenderTH.daemon = True
    dataSenderTH.start()
    time.sleep(0.1)

    commanderTH = threading.Thread(target=self.robotCommander)
    commanderTH.daemon = True
    commanderTH.start()
    time.sleep(0.1)

  def setEventHandler(self, event, func):
    if event in self.eventHandlerDic:
      print("Event ", event, " already exist lisntener")
    else:
      self.eventHandlerDic[event] = func

  def removeEventHandler(self, event):
    if event in self.eventHandlerDic:
      del self.eventHandlerDic[event]
      print("Event ", event, " is removed")
    else:
      print("Event ", event, " not exist lisntener")
  
  def dataGetter(self):
    while True:
      for key, value in self.eventHandlerDic.items():
        if key is Events.FLOOR_IR_EVENT:
          self.analog_read( [FLOOR_IR_1_PIN, FLOOR_IR_2_PIN, FLOOR_IR_3_PIN, FLOOR_IR_4_PIN, FLOOR_IR_5_PIN] )
        elif key is Events.FRONT_IR_EVENT:
          self.digital_read( [145] )
        elif key is Events.SONAR_EVENT:
          self.sonar_read()

      time.sleep(0.1)

  def serialReceiver(self):
    while True:
      recv = self.serialPort.read()
      for i in range(len(recv)):
        self.serialBuf.put(recv[i])
#      for c in self.serialPort.read():
        # print( repr(c) )
#        self.serialBuf.put( ord(c) )

      # time.sleep(0.1)
        
  def serialParser(self):
    step = 0
    parseChar = 0x00
    ins = 0x00
    leng = 0x00
    data = []

    while True:
      if self.serialBuf.qsize() == 0 :
        continue

      parseChar = self.serialBuf.get()
      # print( "step : ",step," parse : ", parseChar)
      if step == 0:
        if parseChar == 0xF0:
          step = 1
      elif step == 1:
        if parseChar == 0x01:
          step = 2
        elif parseChar == 0x63:
          step = 12
        else:
          step = 1
      elif step == 2:
        if (parseChar == 0x00) or (parseChar == 0x01) or (parseChar == 0x02):
          ins = parseChar
          step = 3
        else:
          step = 0
      elif step == 3:
        if parseChar != 0x00:
          leng = parseChar
          del data[:]

          step = 4
        else:
          step = 0
      elif step == 4:
        if len(data) == (leng - 1):
          data.append( parseChar )
          step = 5
        else:
          data.append( parseChar )
      elif step == 5:
        if parseChar == 0xF7:
          if ins == 0x00:
            if data[0] != 0x91:
              step = 0
            self.front_ir_1 = ( ( int(data[1] ) >> 5) & 0x01)
            self.front_ir_2 = ( ( int(data[1] ) >> 6) & 0x01)
          if ins == 0x01:
            for i in range( 0, len(data), 3):
              if data[i] == 0xE1:
                self.floor_ir_1 = data[i + 1]
              elif data[i] == 0xE2:
                self.floor_ir_2 = data[i + 1]
              elif data[i] == 0xE3:
                self.floor_ir_3 = data[i + 1]
              elif data[i] == 0xE6:
                self.floor_ir_4 = data[i + 1]
              elif data[i] == 0xE7:
                self.floor_ir_5 = data[i + 1]
        step = 0
        ins = 0x00
        leng = 0x00
        del data[:]
      elif step == 12:
        if parseChar == 0x0C:
          step = 13
        else:
          step = 0
      elif step == 13:
        if parseChar != 0x07:
          self.sonarLSB = parseChar
          step = 14
        else:
          step = 0
          self.sonarLSB = 0
          self.sonarMSB = 0
      elif step == 14:
        if parseChar != 0x07:
          self.sonarMSB = parseChar
          step = 15
        else:
          step = 0
          self.sonarLSB = 0
          self.sonarMSB = 0
      elif step == 15:
        if parseChar == 0x07:
          self.sonar_1 = self.sonarMSB * 127 + self.sonarLSB
        else:
          step = 0
          self.sonarLSB = 0
          self.sonarMSB = 0

        step = 0
        ins = 0x00
        leng = 0x00
        del data[:]
              
  def dataSender(self):
    while True:
      if Events.FLOOR_IR_EVENT in self.eventHandlerDic:
        ecd = EventCallbackData()
        ecd.floor_ir_1 = self.floor_ir_1
        ecd.floor_ir_2 = self.floor_ir_2
        ecd.floor_ir_3 = self.floor_ir_3
        ecd.floor_ir_4 = self.floor_ir_4
        ecd.floor_ir_5 = self.floor_ir_5

        self.eventHandlerDic[Events.FLOOR_IR_EVENT](ecd)

      if Events.FRONT_IR_EVENT in self.eventHandlerDic:
        ecd = EventCallbackData()
        ecd.front_ir_1 = self.front_ir_1
        ecd.front_ir_2 = self.front_ir_2

        self.eventHandlerDic[Events.FRONT_IR_EVENT](ecd)

      if Events.SONAR_EVENT in self.eventHandlerDic:
        ecd = EventCallbackData()
        ecd.distance = self.sonar_1

        self.eventHandlerDic[Events.SONAR_EVENT](ecd)

      time.sleep(0.1)

  def portOpen(self, serial_dir):
    self.serialPort = serial.Serial( serial_dir, baudrate=115200)
    # , parity=Serial.PARITY_NONE, stopbits=serial.STOPBITS_ONE, bytesize=seiral.EIGHTBITS 

    if self.pinModeInit() is False:
      return False
    print('Pin mode init done')

    if self.syntexInit() is False:
      return False
    print('Sysex init done')

    return True

  def pinModeInit(self):
    # initPacket = []

    try:
      for number, data in self.pins.items():
        initPacket = [ 0xF4, number, data.mode]
        # initPacket.append(0xF4)
        # initPacket.append(number)
        # initPacket.append(data.mode)
        self.serialPort.write(initPacket)
    except:
      print('Pin mode init error : Pin map data error')
      return False

    return True

  def syntexInit(self):
    try:
      for number, data in self.pins.items():
        if data.mode == 2:
          continue
        elif data.mode == 4:
          self.servoInit(number, data.minPulse, data.maxPulse)
        elif data.mode == 14:
          self.pixelLEDInit(number, data.moduleCount)
        time.sleep(0.05)
    except:
      print('Syntex init error : Syntex map data error')
      return False
    
    return True

  #  =================== CONTROL FUNC  =================== #
  def robotCommander(self):
    while True:
      if self.contorlBuf.qsize() == 0 :
        time.sleep(0.01)
        continue

      c = self.contorlBuf.get()
      
      if self.wheelType == Wheels.NORMAL:
        self.controlNormal( c[0], c[1])
      elif self.wheelType == Wheels.MECANUM:
        self.controlMecanum( c[0], c[1], c[2] )
      elif self.wheelType == Wheels.OMNI:
        self.controlOmni( c[0], c[1], c[2] )

      time.sleep( c[3] * 0.001 )

  def control(self, linX, linY, angY):
    self.contorlBuf.put( [linX, linY, angY, 0] )
  
  def controlWhile(self, linX, linY, angY, ms):
    self.contorlBuf.put( [linX, linY, angY, ms] )

  def controlNormal(self, linX, linY):
    if linX == 0 and linY == 0 :
      self.driveStop()
    elif linX != 0 and linY == 0 :
      self.driveFB(linX)
    elif linX == 0 and linY != 0 :
      self.rotateLR(linY)
    elif linX != 0 and linY != 0 :
      self.driveCurve(linX, linY)
  
  def controlMecanum(self, linX, linY, angY):
    if( linX == 0 and linY == 0 and angY == 0) :
      self.driveStop()
    elif( linX != 0 and linY == 0 and angY == 0 ) :
      self.driveFB(linX)
    elif( linX == 0 and linY != 0 and angY == 0 ) :
      self.driveLR(linY)
    elif( linX == 0 and linY == 0 and angY != 0 ) :
      self.rotateLR(angY)
    elif( linX != 0 and linY != 0 and angY == 0 ) :
      self.driveDiagonal(linX, linY)
  
  def driveStop(self):
    self.dcmotor_write(MOTOR_LF, 0, 0)
    self.dcmotor_write(MOTOR_LD, 0, 0)
    self.dcmotor_write(MOTOR_RF, 0, 0)
    self.dcmotor_write(MOTOR_RD, 0, 0)

  def driveFB(self, level):
    if( level > 0 ):
      self.dcmotor_write(MOTOR_LF, MOTOR_L_F, level)
      self.dcmotor_write(MOTOR_LD, MOTOR_L_F, level)
      self.dcmotor_write(MOTOR_RF, MOTOR_R_F, level)
      self.dcmotor_write(MOTOR_RD, MOTOR_R_F, level)
    else:
      self.dcmotor_write(MOTOR_LF, MOTOR_L_D, level* -1)
      self.dcmotor_write(MOTOR_LD, MOTOR_L_D, level* -1)
      self.dcmotor_write(MOTOR_RF, MOTOR_R_D, level* -1)
      self.dcmotor_write(MOTOR_RD, MOTOR_R_D, level* -1)

  def driveLR(self, level):
    if( level > 0 ):
      self.dcmotor_write(MOTOR_LF, MOTOR_L_D, level)
      self.dcmotor_write(MOTOR_LD, MOTOR_L_F, level)
      self.dcmotor_write(MOTOR_RF, MOTOR_R_F, level)
      self.dcmotor_write(MOTOR_RD, MOTOR_R_D, level)
    else:
      self.dcmotor_write(MOTOR_LF, MOTOR_L_F, level * -1)
      self.dcmotor_write(MOTOR_LD, MOTOR_L_D, level * -1)
      self.dcmotor_write(MOTOR_RF, MOTOR_R_D, level * -1)
      self.dcmotor_write(MOTOR_RD, MOTOR_R_F, level * -1)

  def rotateLR(self, level):
    if( level > 0 ) :
      self.dcmotor_write(MOTOR_LF, MOTOR_L_F, level)
      self.dcmotor_write(MOTOR_LD, MOTOR_L_F, level)
      self.dcmotor_write(MOTOR_RF, MOTOR_R_D, level)
      self.dcmotor_write(MOTOR_RD, MOTOR_R_D, level)
    else:
      self.dcmotor_write(MOTOR_LF, MOTOR_L_D, level * -1)
      self.dcmotor_write(MOTOR_LD, MOTOR_L_D, level * -1)
      self.dcmotor_write(MOTOR_RF, MOTOR_R_F, level * -1)
      self.dcmotor_write(MOTOR_RD, MOTOR_R_F, level * -1)

  def driveCurve(self, xlevel, ylevel):
    if( xlevel > 0 ):
      #  right turn
      if( ylevel > 0 ):
        self.dcmotor_write(MOTOR_LF, MOTOR_L_F, xlevel)
        self.dcmotor_write(MOTOR_LD, MOTOR_L_F, xlevel)
        self.dcmotor_write(MOTOR_RF, MOTOR_R_F, (xlevel + ylevel))
        self.dcmotor_write(MOTOR_RD, MOTOR_R_F, (xlevel + ylevel))
      #  left turn
      else:
        self.dcmotor_write(MOTOR_LF, MOTOR_L_F, (xlevel + ylevel))
        self.dcmotor_write(MOTOR_LD, MOTOR_L_F, (xlevel + ylevel))
        self.dcmotor_write(MOTOR_RF, MOTOR_R_F, xlevel)
        self.dcmotor_write(MOTOR_RD, MOTOR_R_F, xlevel)
    else:
      #  right turn
      if( ylevel > 0 ):
        self.dcmotor_write(MOTOR_LF, MOTOR_L_D, xlevel)
        self.dcmotor_write(MOTOR_LD, MOTOR_L_D, xlevel)
        self.dcmotor_write(MOTOR_RF, MOTOR_R_D, (xlevel + ylevel))
        self.dcmotor_write(MOTOR_RD, MOTOR_R_D, (xlevel + ylevel))
      #  left turn
      else:
        self.dcmotor_write(MOTOR_LF, MOTOR_L_D, (xlevel + ylevel))
        self.dcmotor_write(MOTOR_LD, MOTOR_L_D, (xlevel + ylevel))
        self.dcmotor_write(MOTOR_RF, MOTOR_R_D, xlevel)
        self.dcmotor_write(MOTOR_RD, MOTOR_R_D, xlevel)

  def driveDiagonal(self, xlevel, ylevel):
    if( xlevel > 0 ):
      if( ylevel > 0 ):
        self.dcmotor_write(MOTOR_LD, MOTOR_L_F, xlevel + ylevel)
        self.dcmotor_write(MOTOR_RF, MOTOR_R_F, xlevel + ylevel)
      else:
        self.dcmotor_write(MOTOR_LF, MOTOR_L_F, xlevel + ylevel)
        self.dcmotor_write(MOTOR_RD, MOTOR_R_F, xlevel + ylevel)
    else:
      if( ylevel > 0 ):
        self.dcmotor_write(MOTOR_LF, MOTOR_L_D, xlevel + ylevel)
        self.dcmotor_write(MOTOR_RD, MOTOR_R_D, xlevel + ylevel)
      else:
        self.dcmotor_write(MOTOR_LD, MOTOR_L_D, xlevel + ylevel)
        self.dcmotor_write(MOTOR_RF, MOTOR_R_D, xlevel + ylevel)

  def controlOmni(self, linX, linY, angY):
    if( linX == 0 and linY == 0 and angY == 0):
      self.omniDriveStop()
    elif( linX != 0 and linY == 0 and angY == 0 ):
      self.omniDriveFB(linX)
    elif( linX == 0 and linY != 0 and angY == 0 ):
      self.omniDriveLR(linY)
    elif( linX == 0 and linY == 0 and angY != 0 ):
      self.omniRotateLR(angY)
    elif( linX != 0 and linY != 0 and angY == 0 ):
      self.omniDriveCurve(linX, linY)

  def omniDriveStop(self):
    self.dcmotor_write2( OMNI_MOTOR_L, 0, 0, OMNI_MOTOR_R, 0, 0, OMNI_MOTOR_T, 0, 0 )

  def omniDriveFB(self, level):
    if( level < 0 ):
      self.dcmotor_write2( OMNI_MOTOR_L, OMNI_MOTOR_D, level * -10, OMNI_MOTOR_R, OMNI_MOTOR_F, level * -10, OMNI_MOTOR_T, 0, 0 )
    else:
      self.dcmotor_write2( OMNI_MOTOR_L, OMNI_MOTOR_F, level * 10, OMNI_MOTOR_R, OMNI_MOTOR_D, level * 10, OMNI_MOTOR_T, 0, 0 )

  def omniDriveLR(self, level):
    if( level > 5 ) and (level < -5):
      tLevel = 10
      rlLevel = 4
    elif( level < 6 ) and (level > 0) and (level > -6) and (level < 0 ):
      tLevel = 7
      rlLevel = 3

    if( level < 0 ):
      self.dcmotor_write2( OMNI_MOTOR_L, OMNI_MOTOR_D, rlLevel * 5, OMNI_MOTOR_R, OMNI_MOTOR_D, rlLevel * 5, OMNI_MOTOR_T, OMNI_MOTOR_F, tLevel * 10 )
    else:
      self.dcmotor_write2( OMNI_MOTOR_L, OMNI_MOTOR_F, rlLevel * 5, OMNI_MOTOR_R, OMNI_MOTOR_F, rlLevel * 5, OMNI_MOTOR_T, OMNI_MOTOR_D, tLevel * 10 )

  def omniRotateLR(self, level):
    if( level < 0 ):
      self.dcmotor_write2( OMNI_MOTOR_L, OMNI_MOTOR_D, level * -10, OMNI_MOTOR_R, OMNI_MOTOR_D, level * -10, OMNI_MOTOR_T, OMNI_MOTOR_D, level * -10 )
    else:
      self.dcmotor_write2( OMNI_MOTOR_L, OMNI_MOTOR_F, level * 10, OMNI_MOTOR_R, OMNI_MOTOR_F, level * 10, OMNI_MOTOR_T, OMNI_MOTOR_F, level * 10 )

  def omniDriveCurve(self, xlevel, ylevel):
    level = (int)( ( abs(xlevel) + abs(ylevel) ) / 2)

    if( xlevel > 0 ):
      if ( ylevel > 0 ):
        dcmotor_write2( OMNI_MOTOR_L, OMNI_MOTOR_F, level * 10, OMNI_MOTOR_R, OMNI_MOTOR_D, 0, OMNI_MOTOR_T, OMNI_MOTOR_D, level * 10 )
      else:
        dcmotor_write2( OMNI_MOTOR_L, OMNI_MOTOR_F, 0, OMNI_MOTOR_R, OMNI_MOTOR_D, level * 10, OMNI_MOTOR_T, OMNI_MOTOR_F, level * 10 )
    else:
      if ( ylevel > 0 ):
        dcmotor_write2( OMNI_MOTOR_L, OMNI_MOTOR_D, 0, OMNI_MOTOR_R, OMNI_MOTOR_F, level * 10, OMNI_MOTOR_T, OMNI_MOTOR_D, level * 10 )
      else:
        dcmotor_write2( OMNI_MOTOR_L, OMNI_MOTOR_D, level * 10, OMNI_MOTOR_R, OMNI_MOTOR_D, 0, OMNI_MOTOR_T, OMNI_MOTOR_F, level * 10 )

  #  =================== LED FUNC  =================== #
  def ledRed(self, id = 0):
    self.pixelled_write( LED_PIN, id, 255, 0, 0)

  def ledGreen(self, id = 0):
    self.pixelled_write( LED_PIN, id, 0, 255, 0)

  def ledBlue(self, id = 0):
    self.pixelled_write( LED_PIN, id, 0, 0, 255)

  def ledYellow(self, id = 0):
    self.pixelled_write( LED_PIN, id, 174, 96, 0)

  def ledWhite(self, id = 0):
    self.pixelled_write( LED_PIN, id, 255, 255, 255)

  def ledOn(self, id = 0, r = 0, g = 0, b = 0):
    self.pixelled_write( LED_PIN, id, r, g, b)

  def ledOff(self, id = 0):
    self.pixelled_write( LED_PIN, id, 0, 0, 0)

  def ledRandom(self, id = 0):
    r = random.randrange(1,255)
    g = random.randrange(1,255)
    b = random.randrange(1,255)

    self.pixelled_write( LED_PIN, id, r, g, b)

  #  =================== REQUST =================== #
  def sonar_read(self):
    packet = []
    packet.append(0xF0)
    packet.append(0x62)
    packet.append(0x0c)
    packet.append(0x0c)
    packet.append(0xff)
    packet.append(0x10)
    packet.append(0x03)
    packet.append(0xf7)

    self.serialPort.write( packet )

  def sensor_read(self, ids):
    packet = []
    packet.append(0xF0)
    packet.append(0x01)
    packet.append(0x02)
    packet.append(len(ids))

    for i in range(0, len(ids)):
      packet.append(ids[i])

    packet.append(0xF7)

    self.serialPort.write( packet )

  def digital_read(self, ids):
    packet = []
    packet.append(0xF0)
    packet.append(0x01)
    packet.append(0x00)
    packet.append(len(ids))

    for i in range(0, len(ids)):
      packet.append(ids[i])

    packet.append(0xF7)

    self.serialPort.write( packet )

    # cout << "cnt : " << w << "  PIN ID : " ;
    # for(int i = 0; i< (sizeof(packet)/sizeof(*packet)); i++)
    # {
    #   cout << hex << setfill('0') << setw(2) << (int)packet[i] << " ";
    # }
    # cout << endl;

  def digital_write(self, id, value):
    packet = []
    packet.append(0xF0)
    packet.append(0x00)
    packet.append(0x00)
    packet.append(0x02)
    packet.append(0x00)
    packet.append( int(id) << 1 | int(value))
    packet.append(0xF7)
    
    self.serialPort.write( packet )

  def analog_read(self, ids):
    packet = []
    packet.append(0xF0)
    packet.append(0x01)
    packet.append(0x01)
    packet.append(len(ids))

    for i in range(0,len(ids)):
      packet.append(ids[i])
    packet.append(0xF7)

    self.serialPort.write( packet )

    # cout << "cnt : " << w << "  PIN ID : " ;//channel << "   ";
    # for(int i = 0; i< (sizeof(packet)/sizeof(*packet)); i++)
    # {
    #   cout << hex << setfill('0') << setw(2) << (int)packet[i] << " ";
    # }
    # cout << endl;

  def analog_write(self, id, value):
    packet = []

    packet.append(0xF0)
    packet.append(0x00)
    packet.append(0x01)
    packet.append(0x03)
    packet.append(0x00)
    packet.append(int( value % 128 ))
    packet.append( (id) << 1 | int(value / 128) )
    packet.append(0xF7)

    self.serialPort.write( packet )

  #  LEFT  CW = 1
  #  RIGHT CW = 0
  def dcmotor_write(self, channel, dir, speed):
    packet = []
    packet.append(0xF0)
    packet.append(0x00)
    packet.append(0x02)
    packet.append(0x02)
    packet.append( int(speed % 128) )
    packet.append( int(channel) << 4)
    packet.append( int(channel) << 4 | int(dir) << 3 | int(speed / 128))
    packet.append(0xF7)

    self.serialPort.write( packet )

    #cout << "cnt : " << w << "  PIN ID : " << channel << "   ";
    #for(int i = 0; i< (sizeof(packet)/sizeof(*packet)); i++)
    #{
    #  cout << hex << setfill('0') << setw(2) << (int)packet[i] << " ";
    #}
    #cout << endl;

  def dcmotor_write2(self, channel1, dir1, speed1, channel2, dir2, speed2, channel3, dir3, speed3):
    packet = []

    packet.append(0xF0)
    packet.append(0x00)
    packet.append(0x02)
    packet.append(0x06)
    packet.append( int(speed1 % 128) )
    packet.append( int(channel1) << 4 | int(dir1) <<3 | int(speed1 / 128))

    packet.append( int(speed2 % 128) )
    packet.append( int(channel2) << 4 | int(dir2) <<3 | int(speed2 / 128))

    packet.append( int(speed3 % 128) )
    packet.append( int(channel3) << 4 | int(dir3) <<3 | int(speed3 / 128))

    packet.append(0xF7)

    self.serialPort.write( packet )

    # cout << "cnt : " << w << "  PIN ID : " << "   ";
    # for(int i = 0; i< (sizeof(packet)/sizeof(*packet)); i++)
    # {
    #   cout << hex << setfill('0') << setw(2) << (int)packet[i] << " ";
    # }
    # cout << endl;

  def servo_write(self, pin, position):
    packet = []

    packet.append(0xF0)
    packet.append(0x00)
    packet.append(0x03)
    packet.append(0x03)
    packet.append(0x00)
    packet.append( int(position % 128) )
    packet.append( int(pin) << 1 | int(position / 128) )
    packet.append(0xF7)

    self.serialPort.write( packet )

  def startmotor_write(self, motorid, wheelflag, control, brakeflag, torque, blue, green, red, position, sign, speed, dir):
    packet = []

    packet.append(0xF0)
    packet.append(0x00)
    packet.append(0x04)
    packet.append(0x03)
    packet.append( int(red) << 6 | int(green) << 5 | int(blue) << 4 | int(torque) << 3 )

    if wheelflag is True:
      packet[4] = (packet[4]) | int(brakeflag) << 1 | int(wheelflag)
      packet.append(int(speed % 128))
      packet.append( int(motorid) << 6 | int(dir) << 1 | int(speed / 128))
    else:
      packet[4] = (packet[4]) | int(control) << 1 | int(wheelflag)
      packet.append( int(position % 128) )
      packet.aapend( int(motorid) << 6 | int(sign) << 1 | int(position / 128))

    packet.append(0xF7)

    self.serialPort.write( packet )

  def stepmotor_write(self, channel, step, dir, speed, actionmode):
    packet = []
    packet.append(0xF0)
    packet.append(0x00)
    packet.append(0x05)
    packet.append(0x02)
    packet.append(int(step % 128))
    packet.append( int(actionmode) << 6 | int(speed) << 5 | int(dir) << 4 | int(channel) << 3 | int(step/128) << 1 )
    packet.append(0xF7)

    self.serialPort.write( packet )

  def pixelled_write(self, pin, id, red, green, blue):
    packet = []

    if id == 0 :
      packet.append(0xF0)
      packet.append(0x00)
      packet.append(0x07)
      packet.append(0x15)
      packet.append(pin)
      packet.append(0x00)
      packet.append(int(red % 128))
      packet.append(int(green % 128))
      packet.append(int(blue % 128))
      packet.append( int(blue / 128) << 2 | int(green / 128) << 1 | int(red / 128) )
      packet.append(0x01)
      packet.append(int(red % 128))
      packet.append(int(green % 128))
      packet.append(int(blue % 128))
      packet.append( int(blue / 128) << 2 | int(green / 128) << 1 | int(red / 128) )
      packet.append(0x02)
      packet.append(int(red % 128))
      packet.append(int(green % 128))
      packet.append(int(blue % 128))
      packet.append( int(blue / 128) << 2 | int(green / 128) << 1 | int(red / 128) )
      packet.append(0x03)
      packet.append(int(red % 128))
      packet.append(int(green % 128))
      packet.append(int(blue % 128))
      packet.append( int(blue / 128) << 2 | int(green / 128) << 1 | int(red / 128) )
      packet.append(0xf7)

      self.serialPort.write( packet )
    elif (id > 0) and (id < 4)  :
      packet.append(0xF0)
      packet.append(0x00)
      packet.append(0x07)
      packet.append(0x06)
      packet.append(pin)
      packet.append(id)
      packet.append(int(red % 128))
      packet.append(int(green % 128))
      packet.append(int(blue % 128))
      packet.append( int(blue / 128) << 2 | int(green / 128) << 1 | int(red / 128) )
      packet.append(0xF7)

      self.serialPort.write( packet )

      # cout << "PIN ID : " << pin << "  CNT : " << w << endl;
      # for(int i = 0; i< (sizeof(packet)/sizeof(*packet)); i++)
      # {
      #   cout << hex << setfill('0') << setw(2) << (int)packet[i] << " ";
      # }
      # cout << endl;

  #  =================== Sensor Init =================== #
  def servoInit(self, pinNumber, min, max):
    initPacket = []

    initPacket.append(0xF0)
    initPacket.append(0x70)
    initPacket.append(pinNumber)
    initPacket.append(min % 128)
    initPacket.append(min / 128)
    initPacket.append(max % 128)
    initPacket.append(max / 128)
    initPacket.append(0xF7)

    self.serialPort.write( bytes(initPacket) )

  def pixelLEDInit(self, pinNumber, moduleCount) :
    initPacket = []

    initPacket.append(0xF0)
    initPacket.append(0x00)
    initPacket.append(0x07)
    initPacket.append(2)
    initPacket.append( pinNumber << 1 )
    initPacket.append(moduleCount)
    initPacket.append(0xF7)

    self.serialPort.write( initPacket )

# if __name__ == '__main__':
#   sandwich_baseboard = Sandwich_Baseboard(Wheels.NORMAL, '../pins')
