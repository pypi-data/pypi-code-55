led_bar_instance = None

def get_led_bar(pin):
    """Get static reference to servo motor.

    Parameters:
      pint (int):       Digital connection port (range: [2, 8])
    """

    global led_bar_instance

    if led_bar_instance is None:
        from . import arduino, bargraph

        led_bar_instance = bargraph.led_bar(pin, arduino().connection)

    return led_bar_instance

def set_led_level(pin, level):
    """Light up number of bars indicated

    Parameters:
      pin (int):       Digital connection port (range: [2, 8])
      level (int):      Bars to illuminate (range: [0 10])
    """

    get_led_bar(pin).barSetLevel(level)


def set_led_light(pin, led, brightness):
    """Set brightness level of individual bar

    Parameters:
      pin (int):       Digital connection port (range: [2, 8])
      led (int):       Which bars to control (range: [0 10])
      brightness (float):       Level of brightness for bar (range: [0 1])

"""

    get_led_bar(pin).barSetLed(led, brightness)
