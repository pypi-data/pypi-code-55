import json
from ctypes import *
from time import sleep

from hc_models import NET_DVR_CARD_RECORD, LPNET_DVR_CARD_RECORD, NET_DVR_DEVICEINFO_V40
from utils import load, python_str_to_c_str, c_type_array_to_python_str, set_renturn_type

DEV_IP = '192.168.1.22'
DEV_PORT = 8000

DEV_USER_NAME = 'admin'
DEV_PASSWORD = 'qwe123456'


def print_check(call, result, tag):
    print('------------')
    print('{} result'.format(tag), result)
    err_code = None
    err_msg = None
    ok = result >= 0
    if not ok:
        err_code = call.get_err_code()
        get_err_msg = call.get_err_msg
        get_err_msg = set_renturn_type(get_err_msg, POINTER(c_char * 150))
        # 因为上面已经指定了返回值，这里获得的返回结果是一个POINTER指针
        err_msg = get_err_msg(err_code).contents.value.decode('utf-8')
        print('{} error:'.format(tag), err_code, ';', err_msg)
    print('------------')
    return ok, err_code, err_msg


def test_alarm(call, lUserID):
    """
    布防

    :param call:
    :param lUserID:
    :return:
    """
    dict = {
        'url': 'http://192.168.1.191:8024/driver_spot_education/sign_call/'
    }
    data = json.dumps(dict)
    print(data)
    data_json = python_str_to_c_str(data, 200)
    set_flag = call.set_call_back_fun(1, data_json)
    ok, _, _ = print_check(call, set_flag, 'set_call_back_fun')

    alarm_handle = call.setup_alarm(lUserID, 1)
    ok, _, _ = print_check(call, alarm_handle, 'setup_alarm')

    # sleep(180)
    # sleep(1800)
    sleep(60 * 60 * 5)
    # sleep(5)

    close_flag = call.close_alarm(alarm_handle)
    ok, _, _ = print_check(call, close_flag, 'close_alarm')


if __name__ == '__main__':
    call = load()
    call.init(0)

    ip = python_str_to_c_str(DEV_IP, 129)
    user_name = python_str_to_c_str(DEV_USER_NAME, 64)
    password = python_str_to_c_str(DEV_PASSWORD, 64)

    deviceinfo = NET_DVR_DEVICEINFO_V40()
    lUserID = call.login_v40(ip, DEV_PORT, user_name, password, byref(deviceinfo))
    ok, _, _ = print_check(call, lUserID, 'login')
    if not ok:
        call.clean()
        exit()

    print('设备序列号：', c_type_array_to_python_str(deviceinfo.struDeviceV30.sSerialNumber))

    test_alarm(call, lUserID)

    logout_flag = call.logout(lUserID)
    ok, _, _ = print_check(call, logout_flag, 'logout')

    clean_flag = call.clean()
    ok, _, _ = print_check(call, clean_flag, 'clean')
