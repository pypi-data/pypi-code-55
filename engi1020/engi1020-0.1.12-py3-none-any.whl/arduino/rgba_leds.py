rgba_leds_instance = None

def get_rgba_leds(pin, count):
    """Get static reference to chain of RGB LEDs

    Parameters:
      pint (int):       Digital connection port (range: [2, 8])
      count (int):      Number of LEDs connected
    """

    global rgba_leds_instance

    if rgba_leds_instance is None:
        from . import arduino, chainable_leds

        rgba_leds_instance = chainable_leds.rgba_leds(pin, count, arduino().connection)

    return rgba_leds_instance

def set_led_rgb(pin, count, led, red, green, blue):
    """Set red, green and blue level
        of individual LED

    Parameters:
      pin (int):       Digital connection port (range: [2, 8])
      count (int):     Number of LEDs connected in chain
      led (int):       Which LED to control (range: [0 count-1])
      red (float):       Red in LED colour(range: [0 255])
      green (float):     Green in LED colour (range: [0 255])
      blue (float):      Blue in LED colour (range: [0 255])

"""
    get_rgba_leds(pin, count).rgbLedRGB(led, red, green, blue)


def set_led_hsb(pin, count, led, hue, saturation, brightness):
    """Set hue, saturation and brightness level
        of individual LED

    Parameters:
      pin (int):       Digital connection port (range: [2, 8])
      count (int):     Number of LEDs connected in chain
      led (int):       Which LED to control (range: [0 count-1])
      hue (float):       Hue/colour for LED (range: [0 1])
      saturation (float):       Level of saturation for LED (range: [0 1])
      brightness (float):       Level of brightness for LED (range: [0 1])

"""

    get_rgba_leds(pin, count).rgbLedHSB(led, hue, saturation, brightness)
