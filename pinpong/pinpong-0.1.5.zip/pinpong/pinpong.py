import os
import time
import serial
import platform
import serial.tools.list_ports

from pinpong.base.avrdude import *
from pinpong.base import pymata4

OUTPUT = 0
INPUT = 1
ANALOG = 2
PWM = 3
SERVO = 4
NEOPIXEL = 5

PINPONG_MAJOR=0
PINPONG_MINOR=1
PINPONG_DELTA=5

apins={
  "A0":0,
  "A1":1,
  "A2":2,
  "A3":3,
  "A4":4,
  "A5":5,
}

class PinPong:
  def __init__(self, boardname, port):
    self.boardname = boardname.upper()
    self.port = port
    self._iic_init = False
  def printlogo(self):
    print("""
      ____  _       ____                   
     / __ \(_)___  / __ \____  ____  ____ _
    / /_/ / / __ \/ /_/ / __ \/ __ \/ __ `/
   / ____/ / / / / ____/ /_/ / / / / /_/ / 
  /_/   /_/_/ /_/_/    \____/_/ /_/\__, /  
     v%d.%d.%d  Designed by DFRobot  /____/ 
    """%(PINPONG_MAJOR,PINPONG_MINOR,PINPONG_DELTA))
    
  def connect(self):
    self.printlogo()
    major,minor = self.detect_firmata()
    print("Firmata Firmware verson V%d.%d"%(major,minor))
    if major == 0:
      cwdpath,_ = os.path.split(os.path.realpath(__file__))
      pgm = Burner(self.boardname,self.port)
      if(self.boardname == "UNO"):
        name = platform.platform()
        if name.find("Linux_vvBoard_OS")>0:
          cmd = "/home/scope/software/avrdude-6.3/avrdude -C/home/scope/software/avrdude-6.3/avrdude.conf -v -patmega328p -carduino -P"+self.port+" -b115200 -D -Uflash:w:"+cwdpath + "/base/FirmataExpress.Uno.v001.hex"+":i"
          os.system(cmd)
        else:
          pgm.burn(cwdpath + "/base/FirmataExpress.Uno.v001.hex")
      elif(self.boardname == "LEONARDO"):
        port_list_0 = list(serial.tools.list_ports.comports())
        port_list_2 = port_list_0 = [list(x) for x in port_list_0]
        ser = serial.Serial(self.port,1200,timeout=1)
        ser.close()

        retry = 5
        port = None
        while retry:
          retry = retry - 1
          port_list_2 = list(serial.tools.list_ports.comports())
          port_list_2 = [list(x) for x in port_list_2]
          for p in port_list_2:
            if p not in port_list_0:
              port = p
              break
          if port == None:
            time.sleep(0.5)
          if port:
            print("port=====",port)
            break
        pgm = Burner(self.boardname,port[0])
        pgm.burn(cwdpath + "/base/FirmataExpress.Leonardo.v001.hex")
    time.sleep(2)
    self.board = pymata4.Pymata4(com_port=self.port, baud_rate=115200)
    return True

  def detect_firmata(self):
    ser=serial.Serial(self.port, 115200, timeout=3)
    if(self.boardname == "UNO"):
      time.sleep(3)
    ser.read(ser.in_waiting)
    buf=bytearray(b"\xf0\x79\xf7")
    ser.write(buf)
    res = ser.read(10)
    if len(res) < 3:
      major=0
      minor=0
    elif res[0] == 0xF9:
      major = res[1]
      minor = res[2]
    elif res[0] == 0xF0 and res[1] == 0x79:
      major = res[2]
      minor = res[3]
    else:
      major=0
      minor=0
    ser.close()
    return major,minor

  def pin_mode(self, pin, mode, callback=None):
    if(mode == OUTPUT):
      self.board.set_pin_mode_digital_output(pin)
    elif(mode == INPUT):
      self.board.set_pin_mode_digital_input(pin, callback)
    elif(mode == PWM):
      self.board.set_pin_mode_pwm_output(pin)
    elif(mode == ANALOG):
      self.board.set_pin_mode_analog_input(apins[pin], callback)
    elif(mode == SERVO):
      self.board.set_pin_mode_servo(pin)
    elif(mode == NEOPIXEL):
      self.board.set_pin_mode_neo(pin)

  def write_digital(self, pin, value):
    self.board.digital_pin_write(pin, value)
    time.sleep(0.001)

  def read_digital(self, pin):
    return self.board.digital_read(pin)

  def read_analog(self, pin):
    return self.board.analog_read(apins[pin])

  def write_analog(self, pin, value):
    value = value*0x40
    self.board.pwm_write(pin, value)

  def servo_write_angle(self, pin, value):
    self.board.servo_write(pin, value)

  def neopixel_write(self, pin, value):
    self.board.neopixel_write(pin, value)

  def i2c_readfrom(self, address, register, read_byte):
    if not self._iic_init:
      self.board.set_pin_mode_i2c()
      self._iic_init = True
    return self.board.i2c_read(address, register, read_byte, None)

  def i2c_writeto(self, address, args):
    if not self._iic_init:
      self.board.set_pin_mode_i2c()
      self._iic_init = True
    self.board.i2c_write(address, args)