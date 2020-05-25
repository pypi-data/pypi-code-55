# coding=utf-8

# @Time: 2020/4/14 11:00
# @Auther: liyubin

import re
import os
import time
from super_sweetest.config import BASE_DIR

"""
使用xcodebuild,启动WebDriverAgent托管测试服务
devicename 不建议使用名称：iphone，否则将kill所有iphone名称服务
首次启动需xcode安装 WebDriverAgent app，并授权描述文件
"""


def localtime():
    """获取当前时间"""
    localtime_ = time.asctime(time.localtime(time.time()))
    return localtime_


def get_ios_devices():
    """
    get ios devices
    :return: devices_list  [str,]
    :return: device_desc_list   [dict,dict1]
    """
    ins_devices = 'Instruments -s devices'
    ios_device_text = list(os.popen(ins_devices).readlines())

    device_list = []
    device_desc_list = []
    for devi in ios_device_text:
        device_ = devi.strip('\n')
        if 'Known Devices:' not in device_ and 'Mac' not in device_ and 'Simulator' not in device_:
            version = re.findall(r'[(](.*?)[)]', device_)[0]
            device = device_.split(' (')[0]
            assert device.lower() != 'iphone', '名称不能为：iphone， 请重新设置'
            device_list.append(device)
            device_desc_list.append({'device_name': device, 'version': version})
    print(localtime() + ' --- device list online: {} --- '.format(device_list))
    return device_list, device_desc_list


def logs_path():
    """项目路径 join build_logs"""
    path_ = os.path.join(BASE_DIR, 'build_logs')
    os.mkdir(path_) if not os.path.exists(path_) else path_
    return path_


def get_server_url(devicename):
    """
    获取ios_tagent_server输出信息中ServerURLHere
    :return: server_url
    :用法：connect_device("ios:///" + server_url)
    """

    print("----------- %s Get Server URL ----------------" % devicename)
    build_log = os.path.join(logs_path(), '{}_build_log.txt'.format(devicename))
    with open(build_log, 'rb')as fp:
        build_log = str(fp.read())

    serverurl = re.findall(r"http://(.+?)<-ServerURLHere", build_log)
    if serverurl:
        print("----------- %s ServerURLHere is %s ----------------" % (devicename, serverurl[0]))
        url = serverurl[0]
    else:
        print("----------- %s ServerURLHere is no ----------------" % devicename)
        url = 'retry server'
    return url


def run_ios_tagent_server(iostagen_file, platform, devicename):
    """
    非阻塞方式脱离终端在后台运行托管测试服务："nohup "+build_code
    通过xcodebuild 托管指定的手机的iOS-Tagent测试服务

    :-derivedDataPath：产生的缓存文件放在./output目录下
    :  configuration：编译环境，选择Debug/Release
    :-destination :选择test时的目标设备和系统版本号
    """

    assert devicename.lower() != 'iphone', '名称不能为：iphone， 请重新设置'
    build_log = os.path.join(logs_path(), '{}_build_log.txt'.format(devicename))
    # 实时写入日志
    build_code = "xcodebuild test \
                 -project %s/WebDriverAgent.xcodeproj \
                 -scheme WebDriverAgentRunner  \
                 -destination 'platform=%s,name=%s' > $'%s'" % (
        iostagen_file, platform, devicename, build_log)

    print("----------- %s WebDriverAgent Server Start ----------------" % devicename)
    # 非阻塞方式脱离终端在后台运行托管测试服务
    os.popen("nohup %s &" % build_code)
    time.sleep(15)


def kill_ios_tagent_server(devicename):
    """
    kill devicename 对应的WebDriverAgentRunner服务进程
    非阻塞
    """

    assert devicename.lower() != 'iphone', '名称不能为：iphone， 请重新设置'
    print("----------- %s WebDriverAgent Server Stop ----------------" % devicename)
    kill_code = "ps -ef | grep '%s' | grep -v grep | awk '{print $2}' | xargs kill -9" % devicename
    os.popen("nohup %s &" % kill_code)

    build_log = os.path.join(logs_path(), '{}_build_log.txt'.format(devicename))
    if os.path.exists(build_log):
        os.remove(build_log)
    time.sleep(10)

# if __name__ == '__main__':
#
#     iostagen_file_ = '/Users/li/projects/ios_project/iOS-Tagent11'
#     platform_ = 'iOS Simulator'  # 模拟器
#     deviceName_ = 'iPhone 11'

# platform_ = 'iOS'
# deviceName_ = 'iPhone7'

# for i in range(1):
#     print(i)
# run_ios_tagent_server(iostagen_file_, platform_, deviceName_)
# print(get_server_url(deviceName_))
# kill_ios_tagent_server(deviceName_)
