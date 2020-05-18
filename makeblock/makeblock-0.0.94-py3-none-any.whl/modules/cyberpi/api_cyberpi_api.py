# Automatic file, do not edit!

module_auto = None
board = None
import time
from . import BaseModuleAuto
from makeblock.protocols.PackData import HalocodePackData

def autoconnect():
    global module_auto
    if module_auto is None:
        module_auto = BaseModuleAuto(board)
        # blocking to wait cyberpi start  
        board.broadcast()

        board.call(HalocodePackData.broadcast())

def get_mac_address():
    autoconnect()
    return module_auto.get_value("79b023fb7e007b2291a54784c3ab045f", ())

def get_battery():
    autoconnect()
    return module_auto.get_value("3988e0aab4777855379065fc8da2ba34", ())

def get_firmware_version():
    autoconnect()
    return module_auto.get_value("84130d80d8bd240c93e5809565d4fb93", ())

def get_ble():
    autoconnect()
    return module_auto.get_value("3636689f7387305b262ef85f68736204", ())

def get_name():
    autoconnect()
    return module_auto.get_value("974853ae311b0874fd141e4dbc7ea504", ())

def set_name(name):
    autoconnect()
    return module_auto.get_value("3d43914582aed35b01093bddb465dc5a", (name))

def get_brightness():
    autoconnect()
    return module_auto.get_value("69d00a7b2ddc1d85e7ed380663f01ecf", ())

def get_bri():
    autoconnect()
    return module_auto.get_value("04eeffd3a88cf7eee2bf0cb141518cfd", ())

def get_loudness(mode = "maximum"):  
    autoconnect()
    return module_auto.get_value("2469bdefeb4529102292af589e8a2efc", (mode ))

def is_tiltback():
    autoconnect()
    return module_auto.get_value("4cf92569435ea2828f6e3b6304907430", ())

def is_tiltforward():
    autoconnect()
    return module_auto.get_value("aeefd935140b9ce16ede5da7b7ada9fa", ())

def is_tiltleft():
    autoconnect()
    return module_auto.get_value("a4cf641a79cf925a87725098646118f9", ())

def is_tiltright():
    autoconnect()
    return module_auto.get_value("fec52f5ad18094161cec1b417c7e10f5", ())

def is_faceup():
    autoconnect()
    return module_auto.get_value("43c455ca4f76e8a737618fbef054bdbe", ())

def is_facedown():
    autoconnect()
    return module_auto.get_value("c6830cf56b1a4f9aaee9ab53e89a923d", ())

def is_stand():
    autoconnect()
    return module_auto.get_value("c1fb2bd86ac930a853470c2e99c81ea2", ())

def is_handstand():
    autoconnect()
    return module_auto.get_value("c6d9801ca9be3f1032f2be41538fa658", ())

def is_shake():
    autoconnect()
    return module_auto.get_value("c33fcd8e57ae1e3b4c513f6f3386b4b6", ())

def is_waveup():
    autoconnect()
    return module_auto.get_value("e880c1ca448156bf3f371490414e4ee8", ())

def is_wavedown():
    autoconnect()
    return module_auto.get_value("aefc483bd0bcd4561ee6d6d2abface7c", ())

def is_waveleft():
    autoconnect()
    return module_auto.get_value("2dd513e5fbaf94cfe7cafdc64ebbeb74", ())

def is_waveright():
    autoconnect()
    return module_auto.get_value("231b8c48c8b30f532899415153ce868e", ())

def is_clockwise():
    autoconnect()
    return module_auto.get_value("fe32241d6feac2a268f7eafa488761eb", ())

def is_anticlockwise():
    autoconnect()
    return module_auto.get_value("196145516d82a638b39657e5b657df7c", ())

def get_shakeval():
    autoconnect()
    return module_auto.get_value("8a5db13c5c596e0407aa4abbe4f1db48", ())

def get_wave_angle():
    autoconnect()
    return module_auto.get_value("1632d0eb591aed54c5762a5dcdab81ed", ())

def get_wave_speed():
    autoconnect()
    return module_auto.get_value("822687ed58d16f303cc79e0b03bb6ce4", ())

def get_roll():
    autoconnect()
    return module_auto.get_value("1ff145c62ee8412c628e0b0a16fd67fc", ())

def get_pitch():
    autoconnect()
    return module_auto.get_value("36119451128173ff12497681ec2502e4", ())

def get_yaw():
    autoconnect()
    return module_auto.get_value("6bc201e4c360195c6ef04a99c3adb982", ())

def reset_yaw():
    autoconnect()
    return module_auto.common_request("8f4ae00969ac36f47100a06eee0d5046", () ,30)

def get_acc(axis):
    autoconnect()
    return module_auto.get_value("c9f33e1c6b89d173924779a21a9b1019", (axis))

def get_gyro(axis):
    autoconnect()
    return module_auto.get_value("55ddb68e0c157494d0f7e9825815ed43", (axis))

def get_rotation(axis):
    autoconnect()
    return module_auto.get_value("57f3a0363bf3394221b09dd8c8667892", (axis))

def reset_rotation(axis= "all"):
    autoconnect()
    return module_auto.get_value("2e150de47aabc09be2cd468491e39a37", (axis))



class controller_c():

    def is_press(self, id):
        autoconnect()
        return module_auto.get_value("0f4008600f10c30d9500bf0896cb3945", ( id))

    def get_count(self, index):
        autoconnect()
        return module_auto.get_value("f57ae52200b5f46041c7804eec7e0423", ( index))

    def reset_count(self, index):
        autoconnect()
        return module_auto.common_request("87aca6f56a1f74eab8abb4c29616ad3c", ( index) ,30)

controller=controller_c()


class audio_c():

    def play(self, music_name):
        autoconnect()
        return module_auto.common_request("99350cd953df88e5f025bcef34113717", ( music_name))

    def play_until(self, music_name):
        autoconnect()
        return module_auto.common_request("0fd6e3524a5e7c70ccb4ae7194c3ebd4", ( music_name) ,30)

    def record(self):
        autoconnect()
        return module_auto.common_request("8bd7053a4dd190e81637918be72deb46", ())

    def stop_record(self):
        autoconnect()
        return module_auto.common_request("e5e11eee2dfa73a8626ad875188ce3ca", ())

    def play_record(self):
        autoconnect()
        return module_auto.common_request("a8d3656533d5343390a4545985c40c5d", () ,30)

    def play_tone(self, freq, t):
        autoconnect()
        return module_auto.common_request("611cfa431119957e2345e9db178252c6", ( freq, t) ,30)

    def play_drum(self, type, beat):
        autoconnect()
        return module_auto.common_request("db5f575f0e9b43a42505970665e7f263", ( type, beat) ,30)

    def play_music(self, note, beat, type = "piano"):
        autoconnect()
        return module_auto.common_request("3a5b01ef1cc7cf8d5eb05aa275ab0d3f", ( note, beat, type ) ,30)

    def play_note(self, note, beat):
        autoconnect()
        return module_auto.common_request("487b1f0a257ab4cad6edd09ea1df35a0", ( note, beat) ,30)

    def add_tempo(self, pct):
        autoconnect()
        return module_auto.common_request("7cf9bc83ad4148ac607d266d30a4d873", ( pct))

    def set_tempo(self, pct):
        autoconnect()
        return module_auto.common_request("97f80d0c8e36537051d6c9b21e8a7e56", ( pct))

    def get_tempo(self):
        autoconnect()
        return module_auto.get_value("0b4dbd2d04bdaac5cf2f578c6087d58d", ())

    def add_vol(self, val):
        autoconnect()
        return module_auto.common_request("f4b0497ab889a85a865a7486dc9c3b20", ( val))

    def set_vol(self, val):
        autoconnect()
        return module_auto.common_request("c2e5e981c561ba61d2d757a61ff17baa", ( val))

    def get_vol(self):
        autoconnect()
        return module_auto.get_value("4dedceaadf514a624dea51612e1d3f31", ())

    def stop(self):
        autoconnect()
        return module_auto.common_request("510b2145fdd0714503879cc98c435d81", ())

audio=audio_c()


class display_c():

    def set_brush(self, r, g, b):
        autoconnect()
        return module_auto.common_request("3b6fa373ef8ec0614b60949d7a6498eb", ( r, g, b))

    def set_title_color(self, r, g, b):
        autoconnect()
        return module_auto.common_request("f5d5d6501e3afd18d87e81b0ec5eadb4", ( r, g, b))

    def rotate_to(self, angle):
        autoconnect()
        return module_auto.common_request("702530b11223d816f2a79852a5298b7c", ( angle) ,30)

    def off(self):
        autoconnect()
        return module_auto.common_request("064b32a98954fee5dba9c08ce8e9ad37", ())

display=display_c()


class console_c():

    def clear(self):
        autoconnect()
        return module_auto.common_request("dbeeb276871d7a91b2466c5fc9c02222", () ,30)

    def print(self, message):
        autoconnect()
        return module_auto.common_request("5d64cc86824e28e871fb85902181ff18", ( message))

    def println(self, message):
        autoconnect()
        return module_auto.common_request("778c0e54274e093926b2012fa3cc6ba4", ( message))

console=console_c()


class chart_c():

    def set_name(self, name):
        autoconnect()
        return module_auto.common_request("fb465e33a0d73e1ff32e945c30f12836", ( name))

    def clear(self):
        autoconnect()
        return module_auto.common_request("e2c4c0b767853bfb5254e88235ce635b", ())

chart=chart_c()


class linechart_c():

    def add(self, data):
        autoconnect()
        return module_auto.common_request("9c7c0606827e5299122c6b71119a8bab", ( data))

linechart=linechart_c()


class barchart_c():

    def add(self, data):
        autoconnect()
        return module_auto.common_request("953af5bbd66750092d3a1406d53399f3", ( data))

barchart=barchart_c()


class excel_c():

    def add(self, row, column, data):
        autoconnect()
        return module_auto.common_request("619c6b6529423a26de285696190a8c5c", ( row, column, data))

excel=excel_c()


class led_c():

    def on(self, r, g, b, id = "all"):
        autoconnect()
        return module_auto.common_request("5119428dbfeb589dac36fb628ca9248d", ( r, g, b, id ))

    def play(self, name = "rainbow"):
        autoconnect()
        return module_auto.common_request("0c6872183c51d59d859becb64667c349", ( name ) ,30)

    def show(self, color, offset = 0):
        autoconnect()
        return module_auto.common_request("c1de77fafa5b4a4e059515b451a5378d", ( color, offset ))

    def move(self, offset = 1):
        autoconnect()
        return module_auto.common_request("3164e897ffb74c0994c83a84f4938989", ( offset ))

    def off(self, id = "all"):
        autoconnect()
        return module_auto.common_request("883bd62fb06060130e7da7ef5eb29eb6", ( id ))

    def add_bri(self, brightness):
        autoconnect()
        return module_auto.common_request("12d6db993b5874c141e65e740383fd09", ( brightness))

    def set_bri(self, brightness):
        autoconnect()
        return module_auto.common_request("8fd93cf231967274847b712d132b2647", ( brightness))

    def get_bri(self, brightness):
        autoconnect()
        return module_auto.common_request("f32939dd291b3df36b000e28357ec849", ( brightness))

led=led_c()


class wifi_c():

    def connect(self, ssid, password):
        autoconnect()
        return module_auto.common_request("bd1de88cc76a8dbff3a0adea09a34234", ( ssid, password))

    def is_connect(self):
        autoconnect()
        return module_auto.get_value("f0b19cff8669fd061bf3bf8d755a9eee", ())

wifi=wifi_c()


class cloud_c():

    def setkey(self, key):
        autoconnect()
        return module_auto.common_request("8161e0b45af7e1d12e2bd714b8b3d47f", ( key))

    def weather(self, location):
        autoconnect()
        return module_auto.common_request("434de984f1ad299d904e3deb2cb002e2", ( location) , 30)

    def air(self, option, location):
        autoconnect()
        return module_auto.common_request("402dae9adbacff802492236ba6c977c2", ( option, location) , 30)

    def time(self, location):
        autoconnect()
        return module_auto.common_request("70279bf87312616ec7e74ab28530fb32", ( location) , 30)

    def listen(self, language, t):
        autoconnect()
        return module_auto.common_request("97adee4bd25bc6c77195451d5e7a42d6", ( language, t) , 30    )

    def listen_result(self):
        autoconnect()
        return module_auto.common_request("10b07f3c97a2833abaeea5b42aa892b7", () , 30)

    def tts(self, language, message):
        autoconnect()
        return module_auto.common_request("093cf48163eb9ae0997ea9f6a521c2f2", ( language, message) , 30)

    def translate(self, language, message):
        autoconnect()
        return module_auto.common_request("716553fa3b4c7469133cf3d465536cd5", ( language, message) , 30)

cloud=cloud_c()


class timer_c():

    def get(self):
        autoconnect()
        return module_auto.get_value("5535075a55d873b7450bad031ba3ba72", ())

    def reset(self):
        autoconnect()
        return module_auto.common_request("e5359d1a429dbef33644fa7d5e450ab2", ())

def broadcast(message):
    autoconnect()
    return module_auto.common_request("973eab065d5f700522b11bff0540f19a", (message))

def broadcast_and_wait(message):
    autoconnect()
    return module_auto.common_request("fe662895f3ea37bdb913466a5b6ba520", (message))

timer=timer_c()


class wifi_broadcast_c():

    def set(self, message, value):
        autoconnect()
        return module_auto.common_request("e0b9fb05284e48b4d7a4a97c25eca5de", ( message, value) ,30)

    def get(self, message):
        autoconnect()
        return module_auto.common_request("f125d69e4401eb06e48ccd6bb3d6c895", ( message))

wifi_broadcast=wifi_broadcast_c()


class upload_broadcast_c():

    def set(self, message, value):
        autoconnect()
        return module_auto.common_request("71de891af2a5dcbb9a8f4ed958060137", ( message, value) ,30)

    def get(self, message):
        autoconnect()
        return module_auto.common_request("4b09d734021e25bcf990c7896f0ed816", ( message))

upload_broadcast=upload_broadcast_c()


class cloud_broadcast_c():

    def set(self, message, value):
        autoconnect()
        return module_auto.common_request("91f7a4c19cdcf0592e368049f5cb04ea", ( message, value) ,30)

    def get(self, message):
        autoconnect()
        return module_auto.common_request("d51ad9449c1a722b7df593a3ea603ee0", ( message))

def stop_this():
    autoconnect()
    return module_auto.common_request("026f484ae8d9f995e168172504962a25", () ,30)

def stop_other():
    autoconnect()
    return module_auto.common_request("1b05ec802d435cdc23aa16b23bbbc083", () ,30)

def stop_all():
    autoconnect()
    return module_auto.common_request("b74a8ad1b60ed48e72f89272dbfe394d", () ,30)

def restart():
    autoconnect()
    return module_auto.common_request("7801409efa2cbc182d240320f247cf63", () ,30)

cloud_broadcast=cloud_broadcast_c()


class event_c():

    def start(self):
        autoconnect()
        return module_auto.common_request("adc31e0c8c68dd42ab1dad5714a694e2", ())

    def is_shake(self):
        autoconnect()
        return module_auto.common_request("858fcd1af422110143a648486c603c09", ())

    def is_press(self, id):
        autoconnect()
        return module_auto.common_request("e139a21c5116ec7210dbba7476adda02", ( id))

    def is_tiltup(self):
        autoconnect()
        return module_auto.common_request("ed60fa45fd0a9e980401c53e708ded47", ())

    def is_tiltdown(self):
        autoconnect()
        return module_auto.common_request("ba90bda5350a58507a3599c6b0bc8e70", ())

    def is_tiltleft(self):
        autoconnect()
        return module_auto.common_request("357740cb5c8e299bb56f973fddc041f0", ())

    def is_tiltright(self):
        autoconnect()
        return module_auto.common_request("bc4c66390735049c9915db0ceb54dfd2", ())

    def is_faceup(self):
        autoconnect()
        return module_auto.common_request("3a522da87cc3efd0a39364f5bab8d86b", ())

    def is_facedown(self):
        autoconnect()
        return module_auto.common_request("c00c1e0ef54e7541ce8d12b330c3018d", ())

    def is_stand(self):
        autoconnect()
        return module_auto.common_request("68f2fb7b73828e5f82f60501b3aca418", ())

    def is_handstand(self):
        autoconnect()
        return module_auto.common_request("7a4a712ee73877568abfffab4c6a4472", ())

    def is_waveup(self):
        autoconnect()
        return module_auto.common_request("1a1d952a390a09afdab69ba96723a857", ())

    def is_wavedown(self):
        autoconnect()
        return module_auto.common_request("3f5f8108a707d50c9c595b1309913a35", ())

    def is_waveleft(self):
        autoconnect()
        return module_auto.common_request("b0ca4b07b50a6b349fa87608422df1de", ())

    def is_waveright(self):
        autoconnect()
        return module_auto.common_request("ceb37edb2c7c03556f529e45c46a6c79", ())

    def is_clockwise(self):
        autoconnect()
        return module_auto.common_request("a522c41acb057a0eb3955717cfe03993", ())

    def is_anticlockwise(self):
        autoconnect()
        return module_auto.common_request("b6cb8d513b6ac15230e2168434464c70", ())

    def receive(self, message):
        autoconnect()
        return module_auto.common_request("089f1a7ab3ce3d81be1bd167099877bc", ( message))

    def upload_broadcast(self, message):
        autoconnect()
        return module_auto.common_request("92778f090ede75693ab02b31cd72f817", ( message))

    def cloud_broadcast(self, message):
        autoconnect()
        return module_auto.common_request("6a8f93e101547247fb551785ed082bfe", ( message))

    def wifi_broadcast(self, message):
        autoconnect()
        return module_auto.common_request("7027f95df86eacceb065ef8a0493625f", ( message))

    def greater_than(self, threshold, type):
        autoconnect()
        return module_auto.common_request("894ec6719c94b519c18ef380a57d9d82", ( threshold, type))

    def samller_than(self, threshold, type):
        autoconnect()
        return module_auto.common_request("0f372307778f6e742402125956b6e7f4", ( threshold, type))

def set_recognition_url(server = 1, url = "http://msapi.passport3.makeblock.com/ms/bing_speech/interactive"): 
    autoconnect()
    return module_auto.common_request("be139ea20b00673e9e8dcb7bc1640df9", (server , url ))

