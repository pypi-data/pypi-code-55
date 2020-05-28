import time
from pinpong.pinpong import *

class DFRobot_HCSR04:
  def __init__(self,board):
    self.board  = board

  def begin(self, trigger_pin, echo_pin):
    self.trigger_pin = trigger_pin
    self.echo_pin = echo_pin
    self.board.board.set_pin_mode_sonar(self.trigger_pin, self.echo_pin)

  def read(self):
    return self.board.board.sonar_read(self.trigger_pin)[0]