from nanpy.arduinoboard import ArduinoObject
from nanpy.arduinoboard import (arduinoobjectmethod, returns)

class led_bar(ArduinoObject):
    cfg_h_name = 'USE_led_bar'

    def __init__(self, pin, connection=None):
        ArduinoObject.__init__(self, connection=connection)
        self.id = self.call('new', pin)

    @arduinoobjectmethod
    def barSetLevel(self, value):
        pass

    @arduinoobjectmethod
    def barSetLed(self, led, value):
        pass
