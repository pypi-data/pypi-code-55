# coding=utf-8

# @Time: 2020/3/5 10:57
# @Auther: liyubin

import os
import time
import re


"""
android 端独有
appium服务监控和管理
获取已连接手机信息
"""


def localtime():
    """获取当前时间"""
    localtime_ = time.asctime(time.localtime(time.time()))
    return localtime_


def get_devices():
    """
    获取已连接的设备名称
    :return: 返回list
    """
    device_list = []

    adb_devices = 'adb devices'
    devices_texts = list(os.popen(adb_devices).readlines())

    for device in devices_texts:
        device_ = device.strip('\n').split(' ')[0].replace('device', '').replace('\t', '')
        if len(device_) > 0 and device_ != 'List' and 'offline' not in device_:
            device_list.append(device_)
    print(localtime() +' --- device list online: {} --- '.format(device_list))
    return device_list


def get_resolution(devices_name):
    """
    获取当前运行手机分辨率
    return: 返回tuple 传入airtest template
    """
    adb_resolution = 'adb -s {} shell wm size'.format(devices_name)
    resolution_texts = list(os.popen(adb_resolution).readlines())[0]

    resol = resolution_texts.replace('Physical size: ', '').split('x')

    resolution = tuple((int(resol[0]), int(resol[1])))
    # print(localtime() + '--- resolution is : {} ---'.format(resolution))
    return resolution


def get_mobile_name(device_name):
    """
    获取单个手机名称
    :param device_name:
    :return: 反回名称
    """
    adb_mobile = 'adb -s {} shell getprop ro.product.model'.format(device_name)
    mobile_texts = list(os.popen(adb_mobile).readlines())[0]
    mobile = mobile_texts.strip('\n')
    # print(localtime() + '--- mobile is : {} ---'.format(mobile))
    return mobile


def get_physical_density(device_name):
    """
    获取屏幕光学密度
    :param device_name:
    :return: 分辨率值
    """
    adb_physical_density = 'adb -s {} shell wm density'.format(device_name)
    physical_density_texts = list(os.popen(adb_physical_density).readlines())[0]
    physical_density = physical_density_texts.replace('Physical density: ', '').strip('\n')
    # print(localtime() + '--- physical_density is : {} ---'.format(physical_density))
    return physical_density


def get_platform_version(device_name):
    """
    获取手机系统版本
    :param device_name:
    :return: 版本号
    """
    adb_platform_version = 'adb -s {} shell getprop ro.build.version.release'.format(device_name)
    platform_version_texts = list(os.popen(adb_platform_version).readlines())[0]
    platform_version = platform_version_texts.strip('\n')
    # print(localtime() + '--- mobile is : {} ---'.format(mobile))
    return platform_version


# 获取手机信息主方法
def get_mobile_desc(devices_list):
    """
    获取手机的详细信息
    :param devices_list:
    :return: 手机详情[{k:v},{k:v}]
    """
    mobile_desc_list = []
    for device_name in devices_list:

        # 如果未授权就直接反回device_name，不然获取不到设备信息
        if re.search('unauthorized', device_name):
            mobile_desc_list.append({'device_name': device_name, 'mobile_name': device_name})
        else:
            # device_name # 设备名称
            mobile_name = get_mobile_name(device_name)  # 手机名称
            resolution = get_resolution(device_name)  # 分辨率
            physical_density = get_physical_density(device_name)  # 屏幕密度
            platform_version = get_platform_version(device_name)  # 系统版本

            mobile_desc_list.append({'mobile_name': mobile_name, 'device_name': device_name, 'resolution': resolution,
                                     'physical_density': physical_density, 'platform_version': platform_version})

    # print(localtime() + ' --- device list online: {} --- '.format(mobile_desc_list))
    return mobile_desc_list


# appium相关
################################
def find_port_kill_pid(port):
    """
    查找和杀端口的pid
    return: 返回pid循环判断kill
    """
    print(' --- find port %s  --- ' % port)
    find_port = 'netstat -aon | findstr %s' % port
    result = os.popen(find_port)
    text = result.read()
    pid = text[-6:-1]
    print(' --- kill port %s --- ' % port)
    kill_port = 'taskkill -f -pid %s' % pid
    os.popen(kill_port)
    return pid


def kill_all(port=None):
    """
    杀所有appium进程
    """
    if port:
        pid = find_port_kill_pid(port)
    else:
        pid = find_port_kill_pid(5037)  # 模拟器请注释
        # pid = ''
    print(' --- if pid is None kill success ：%s ? --- ' % pid)
    if not pid:
        return True
    for i in range(20):
        print(' --- kill: %s --- ' % pid)
        pid_ = find_port_kill_pid(port)
        if not pid_:
            break


def start_appium_server(port=None):
    """
    启动appium服务，在生成驱动前调用
    """
    if port:
        print(' --- Appium Server Start Port: %s --- ' % port)
        start_ = 'start appium -a 127.0.0.1 -p %s' % port
        os.popen(start_)
    else:
        start_4723 = 'start appium --no-reset --session-override --log ./appium_logs.log'
        print(' --- Appium Server Start Port: %s --- \n --- Create log --- ' % port)
        os.popen(start_4723)
    time.sleep(7)


def stop_appium_server(port=None):
    """
    关闭appium服务，可在关闭驱动后调用
    """
    if port:
        print(' --- Stop Appium Server | Port: %s --- ' % port)
        kill_all(port)
    else:
        print(' --- Stop All Appium Server --- ')
        kill_node = 'taskkill /f /t /im node.exe'
        os.popen(kill_node)
    time.sleep(7)


def exist_port(port):
    """
    查询port 4723 是否被占用，占用就不重复启动appium
    return True 占用
    """
    find_port = 'netstat -aon | findstr %s' % port
    result = os.popen(find_port)
    text = result.read()
    if str(port) not in text:
        return False
    return True


def run_appium_main(port=4723):
    """
    主方法，占用不启动，未占用启动
    """
    status = exist_port(port)
    if not status:
        stop_appium_server(port)

        start_appium_server(port)
    else:
        print(' --- Appium Server Start Raining Now !--- ')


# if __name__ == '__main__':
#     stop_appium_server(4723)
#     print(get_devices())
#     sync_devices('http://192.168.18.129:80/')
