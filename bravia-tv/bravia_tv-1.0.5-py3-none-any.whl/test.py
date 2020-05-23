import logging
from braviarc import BraviaRC
from time import sleep

_LOGGER = logging.getLogger(__name__)

ip_address = '192.168.1.102'
tv = BraviaRC(ip_address)

pin = '0146'
tv.connect(pin, 'my_device_id', 'my device name')
if tv.is_connected():
    #print(tv.get_audio_outputs())
    #print(tv.mute_volume(True))
    #print(tv.get_volume_info())
    # print(tv.mute_volume())
    # print(tv.get_volume_info())
    # print(tv.mute_volume())
    # print(tv.volume_up())
    # print(tv.get_volume_info())
    # print(tv.volume_down())
    # print(tv.get_volume_info())
    #for x in tv.get_audio_outputs():
    #    print(tv.set_volume_level(.1, x))
    #    print(tv.get_volume_info(x))
    print(tv.turn_off())
    print(tv.get_power_status())
    sleep(5)
    print(tv.turn_on())
    print(tv.get_power_status())