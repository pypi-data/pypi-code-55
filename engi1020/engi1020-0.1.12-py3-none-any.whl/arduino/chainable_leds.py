from nanpy.arduinoboard import ArduinoObject
from nanpy.arduinoboard import (arduinoobjectmethod, returns)

class rgba_leds(ArduinoObject):
    cfg_h_name = 'USE_rgba_leds'

    def __init__(self, pin, count, connection=None):
        ArduinoObject.__init__(self, connection=connection)
        self.id = self.call('new', pin, count)

    @arduinoobjectmethod
    def rgbLedHSB(self, led, hue, saturation, brightness):
        pass

    @arduinoobjectmethod
    def rgbLedRGB(self, led, red, green, blue):
        pass
