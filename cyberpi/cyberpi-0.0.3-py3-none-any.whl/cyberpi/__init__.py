from makeblock import quit
from makeblock import cyberpi

# for n in cyberpi.__dir__():
#     if n.find("_c")==-1:
#         print(n+" = cyberpi."+n)
time = cyberpi.time
get_mac_address = cyberpi.get_mac_address
get_battery = cyberpi.get_battery
get_firmware_version = cyberpi.get_firmware_version
get_ble = cyberpi.get_ble
get_name = cyberpi.get_name
set_name = cyberpi.set_name
get_brightness = cyberpi.get_brightness
get_bri = cyberpi.get_bri
get_loudness = cyberpi.get_loudness
is_tiltback = cyberpi.is_tiltback
is_tiltforward = cyberpi.is_tiltforward
is_tiltleft = cyberpi.is_tiltleft
is_tiltright = cyberpi.is_tiltright
is_faceup = cyberpi.is_faceup
is_facedown = cyberpi.is_facedown
is_stand = cyberpi.is_stand
is_handstand = cyberpi.is_handstand
is_shake = cyberpi.is_shake
is_waveup = cyberpi.is_waveup
is_wavedown = cyberpi.is_wavedown
is_waveleft = cyberpi.is_waveleft
is_waveright = cyberpi.is_waveright
is_anticlockwise = cyberpi.is_anticlockwise
get_shakeval = cyberpi.get_shakeval
get_wave_angle = cyberpi.get_wave_angle
get_wave_speed = cyberpi.get_wave_speed
get_roll = cyberpi.get_roll
get_pitch = cyberpi.get_pitch
get_yaw = cyberpi.get_yaw
reset_yaw = cyberpi.reset_yaw
get_acc = cyberpi.get_acc
get_gyro = cyberpi.get_gyro
get_rotation = cyberpi.get_rotation
reset_rotation = cyberpi.reset_rotation
controller = cyberpi.controller
audio = cyberpi.audio
display = cyberpi.display
console = cyberpi.console
chart = cyberpi.chart
linechart = cyberpi.linechart
barchart = cyberpi.barchart
excel = cyberpi.excel
led = cyberpi.led
wifi = cyberpi.wifi
cloud = cyberpi.cloud
timer = cyberpi.timer
stop_this = cyberpi.stop_this
stop_other = cyberpi.stop_other
stop_all = cyberpi.stop_all
restart = cyberpi.restart
cloud_broadcast = cyberpi.cloud_broadcast