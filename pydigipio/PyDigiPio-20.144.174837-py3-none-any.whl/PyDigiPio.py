import os


def configure_pin(pin_number: int, direction: str):
    '''Sets pin assigned to GPIO pin_number as "in" or "out"'''
    path = "/sys/class/gpio/gpio{}/direction".format(pin_number)
    if not os.path.isfile(path):
        device = os.open("/sys/class/gpio/export", os.O_WRONLY)
        os.write(device, bytes("{}".format(pin_number), "utf-8"))
        os.close(device)
    device = os.open(path, os.O_WRONLY)
    os.write(device, bytes("{}".format(direction), "utf-8"))
    os.close(device)


def write_to_pin(pin_number: int, value: bool):
    """Set GPIO pin_number True(HIGH) or False(LOW)"""
    device = os.open("/sys/class/gpio/gpio{}/value".format(pin_number), os.O_WRONLY)
    os.write(device, bytes("{}".format(int(value)), "utf-8"))
    os.close(device)


def read_from_pin(pin_number: int) -> bool:
    """Get state of GPIO pin_number, returns True(HIGH) or False(LOW)"""
    device = os.open("/sys/class/gpio/gpio{}/value".format(pin_number), os.O_RDONLY)
    value = int(os.read(device, 1))
    os.close(device)

    return value == 1


def has_permission() -> bool:
    """Check if user has permission to use GPIO"""
    try:
        os.open("/sys/class/gpio/export", os.O_WRONLY)
    except PermissionError:
        return False

    return True
