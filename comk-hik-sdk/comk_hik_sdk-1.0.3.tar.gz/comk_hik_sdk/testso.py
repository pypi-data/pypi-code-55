from ctypes import *

from comk_hik_sdk.hc_models import NET_DVR_CARD_RECORD, LPNET_DVR_CARD_RECORD, NET_DVR_DEVICEINFO_V40
from comk_hik_sdk.utils import load, python_str_to_c_str, c_type_array_to_python_str, set_renturn_type

DEV_IP = '192.168.1.11'
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


def test_set_one_card(call, lUserID, card_no=None, eno=None, name=None):
    """
    创建卡

    :param call:
    :param lUserID:
    :param card_no:
    :param eno:
    :param name:
    :return:
    """
    lHandle = call.start_remote_control(lUserID, 101)
    ok, _, _ = print_check(call, lHandle, 'start_remote')

    print('-------创建卡-----------')
    card_no = python_str_to_c_str('222', 32)
    eno = 20052103  # 限制为8位数以下，否则会报错
    name = python_str_to_c_str('本版本', 32)
    dwState = call.set_one_card(lHandle, card_no, eno, name)
    ok, _, _ = print_check(call, dwState, 'set card')

    end_flag = call.end_remote_control(lHandle)
    ok, _, _ = print_check(call, end_flag, 'end_remote')


def test_get_one_card(call, lUserID, card_no=None):
    """
    获取一张卡

    :param call:
    :param lUserID:
    :param card_no:
    :return:
    """
    lHandle = call.start_remote_control(lUserID, 201)
    ok, _, _ = print_check(call, lHandle, 'start_remote')

    card_record = NET_DVR_CARD_RECORD()
    point = LPNET_DVR_CARD_RECORD(card_record)
    print('-------获取一张卡-----------')
    card_no = python_str_to_c_str('11', 32)

    dwState = call.handle_one_card(lHandle, card_no, point)
    print('dwState', dwState)
    if dwState == 1002:
        print('-----------')
        print('byCardNo:', c_type_array_to_python_str(card_record.byCardNo))
        print('dwEmployeeNo:', card_record.dwEmployeeNo)
        print('byName:', c_type_array_to_python_str(card_record.byName))

    end_flag = call.end_remote_control(lHandle)
    ok, _, _ = print_check(call, end_flag, 'end_remote')


def test_get_all_cards(call, lUserID):
    """
    获取所有卡

    :return:
    """
    lHandle = call.start_remote_control(lUserID, 202)
    ok, _, _ = print_check(call, lHandle, 'start_remote')

    card_record = NET_DVR_CARD_RECORD()
    point = LPNET_DVR_CARD_RECORD(card_record)
    print('-------获取所有卡-----------')
    dwState = call.get_all_card(lHandle, point)
    while dwState == 1000:
        print('-----------')
        print('byCardNo:', c_type_array_to_python_str(card_record.byCardNo))
        print('dwEmployeeNo:', card_record.dwEmployeeNo)
        print('byName:', c_type_array_to_python_str(card_record.byName))
        dwState = call.get_all_card(lHandle, pointer(card_record))

    end_flag = call.end_remote_control(lHandle)
    ok, _, _ = print_check(call, end_flag, 'end_remote')


def test_del_one_card(call, lUserID, card_no=None):
    """
    删除卡

    :param call:
    :param lUserID:
    :param card_no:
    :return:
    """
    lHandle = call.start_remote_control(lUserID, 301)
    ok, _, _ = print_check(call, lHandle, 'start_remote')

    card_record = NET_DVR_CARD_RECORD()
    point = LPNET_DVR_CARD_RECORD(card_record)
    print('-------删除一张卡-----------')
    card_no = python_str_to_c_str('222', 32)

    dwState = call.handle_one_card(lHandle, card_no, point)
    if dwState == 1002:
        print('-----------')
        print('byCardNo:', c_type_array_to_python_str(card_record.byCardNo))

    end_flag = call.end_remote_control(lHandle)
    ok, _, _ = print_check(call, end_flag, 'end_remote')


def test_alarm(call, lUserID):
    """
    布防

    :param call:
    :param lUserID:
    :return:
    """
    set_flag = call.set_call_back_fun(1)
    ok, _, _ = print_check(call, set_flag, 'set_call_back_fun')

    alarm_handle = call.setup_alarm(lUserID)
    ok, _, _ = print_check(call, alarm_handle, 'setup_alarm')

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
    print('设备序列号：', c_type_array_to_python_str(deviceinfo.struDeviceV30.sSerialNumber))

    test_set_one_card(call, lUserID)
    test_get_all_cards(call, lUserID)
    test_get_one_card(call, lUserID)
    test_del_one_card(call, lUserID)
    test_get_all_cards(call, lUserID)

    # test_alarm(call, lUserID)

    logout_flag = call.logout(lUserID)
    ok, _, _ = print_check(call, logout_flag, 'logout')

    clean_flag = call.clean()
    ok, _, _ = print_check(call, clean_flag, 'clean')
