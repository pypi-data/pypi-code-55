"""Arduino API wrapper.

This code assumes that there is only one Arduino device connected.
"""

import nanpy


# Assuming there's only one Arduino connected to this computer, here it is.
a = None

def arduino():
    """Return Arduino API, instantiating if needed."""

    global a

    if a is None:
        port = None

        import sys

        if sys.platform == 'win32':
            #print('Check Windows Device Manager to see which COM the Arduino Uno has been assigned')
            #port = input('Please specify COM port (eg. COM10): ')
            ## code from http://leim.altervista.org/blog/detect-arduino-board-in-python/?doing_wp_cron=1590438741.3099739551544189453125
            import serial.tools.list_ports
            
            ports = list(serial.tools.list_ports.comports())
            Arduino_ports=[]
            for p in ports:
                if 'Arduino' in p.description:
                    Arduino_ports.append(p)
            if len(Arduino_ports)==0:
                print("no Arduino board detected")
                
            if len(Arduino_ports) > 1:
                print('Multiple Arduinos found - using the first')
            else:
                print("Arduino board detected")
             
            if len(Arduino_ports) >= 1:
              print(Arduino_ports[0].device)
              port = Arduino_ports[0].device

        elif sys.platform == 'darwin':
            # Find /dev/cu.usbmodem* using the glob module:
            import glob
            ports = glob.glob('/dev/cu.usbmodem*')

            if len(ports) == 0:
                sys.stderr.write('No Arduino device detected (plugged in?)\n')
                sys.exit(1)

            elif len(ports) == 1:
                port = ports[0]

            else:
                print('Multiple devices detected:')
                for i, name in enumerate(ports):
                    print(f'[{i}]    {name}')

                while port == None:
                    try:
                        i = int(input('select device> '))
                        port = ports[int(i)]

                    except IndexError as e:
                        sys.stderr.write('Invalid device number\n')

                    except ValueError as e:
                        print(e)

        a = nanpy.ArduinoApi(connection=nanpy.SerialManager(device=port))

    return a


def analog_read(pin):
    """Read a value from an analog port.

    Parameters:
      pin (int):     Analog pin to read from (e.g., 2 for A2).

    Returns:         Quantized analog value (0–1023).
    """
    return arduino().analogRead(pin+14)

def analog_write(pin, duty):
    """Write a value to an analog port.

    Parameters:
      pin (int):     Analog pin to write to (e.g., 2 for A2).
      duty (int):    Duty cycle to set (0–255).
    """
    return arduino().analogWrite(pin+14, duty)

def digital_read(pin):
    """Read a value from a digital port.

    Parameters:
      pin (int):     Digital pin to read from (e.g., 4 for D4).

    Returns:         True or False.
    """
    return arduino().digitalRead(pin)

def digital_write(pin, value):
    """Write a value to a digital port.

    Parameters:
      pin (int):     Digital pin to write to (e.g., 4 for D4).
      value (bool):  Value to write (True or False).
    """
    return arduino().digitalWrite(pin, value)


from . import lcd
lcd_clear = lcd.clear
lcd_move_cursor = lcd.move_cursor
lcd_print = lcd.print
lcd_hsv = lcd.hsv
lcd_rgb = lcd.rgb

from . import temperature
temp_celsius = temperature.celsius

from . import motor
servo_move = motor.move
servo_read = motor.read

from . import buzzer
buzzer_note = buzzer.note
buzzer_stop = buzzer.stop

from . import ir_distance
distance_cm = ir_distance.centimeters

from . import led_bar
led_bar_set_level = led_bar.set_led_level
led_bar_set_led_light = led_bar.set_led_light

from . import rgba_leds
rgba_leds_set_rgb = rgba_leds.set_led_rgb
rgba_leds_set_hsb = rgba_leds.set_led_hsb
