# -*- coding:utf-8 -*-
'''
获取软件信息/安装卸载软件
check_minimum_python_version(ver=str): Error（python版本不匹配或者未安装）；python安装路径
check_firefox_version(): None（未安装FF）；FF版本（自动补齐.0）
check_chrome_version(): None（未安装）：chrome版本
check_driver_exist(python_dir, browser_type): 检查对应的driver在python目录下是否存在
unzip_file():解压zip文件到指定目录
is_valid_zip_file():是否为合格的zip文件
'''

import sys
import os
import winreg
import urllib3
import zipfile
import zhangwei_helper.enum.SelfEnum as zw_enum

def check_minimum_python_version(ver=None):
    '''
    :param ver:None或者字符，例如'3.6'
    :return: error或者python安装路径
    '''
    if ver is not None:
        # check the expected version is correct
        tmp = ver.split('.')
        expected_major_ver = int(tmp[0])
        expected_minor_ver = int(tmp[1])
        expected_micro_ver = 0
        if len(tmp) == 3:
            expected_micro_ver = int(tmp[2])

    tmp = sys.version_info
    exist_major_ver = tmp.major
    exist_minor_ver = tmp.minor
    exist_micro_ver = tmp.micro
    exist_ver = '%s.%s.%s' % (tmp.major, tmp.minor, tmp.micro)

    python_ver_match = None
    if ver is not None:
        python_ver_match = False
        if exist_major_ver == expected_major_ver:
            if exist_minor_ver > expected_minor_ver:
                python_ver_match = True
            elif exist_minor_ver == expected_minor_ver:
                if exist_micro_ver >= expected_micro_ver:
                    python_ver_match = True

    if python_ver_match is not None:
        if not python_ver_match:
            raise EnvironmentError('当前python版本' + exist_ver + '不匹配期望的版本' + ver + ',请重新安装')


    try:
        # HKEY_CURRENT_USER\Software\Python\PythonCore\3.8\InstallPath
        sub_item = r'Software\Python\PythonCore\%s.%s\InstallPath' % (exist_major_ver, exist_minor_ver)
        python_item = winreg.OpenKey(winreg.HKEY_CURRENT_USER, sub_item)
    except Exception as e:
        raise EnvironmentError('无法找到python安装路径，请重新安装python%s或者以上版本' % ver)
        # return None

    val, t = winreg.QueryValueEx(python_item, 'ExecutablePath')
    return os.path.dirname(val)


def get_firefox_version():
    '''

    :return:返回最新的firefox版本
    '''
    # HKEY_LOCAL_MACHINE\SOFTWARE\Mozilla\Mozilla Firefox
    try:
        ff_item = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, r'SOFTWARE\Mozilla')
    except Exception as e:
        print('尚未安装firefox')
        return None

    ff_sub_item = winreg.OpenKey(ff_item, r'Mozilla Firefox')
    val, t = winreg.QueryValueEx(ff_sub_item, r'CurrentVersion')
    ff_ver = val.split(' ')[0]
    return ff_ver


def get_chrome_version():
    '''

    :return:None(未安装)；返回最新的chrome版本
    '''
    # HKEY_CURRENT_USER\Software\Google\Chrome\BLBeacon
    # HKEY_CURRENT_USER\Software\Microsoft\Windows\CurrentVersion\Uninstall\Google Chrome
    try:
        chrome_key = winreg.OpenKey(winreg.HKEY_CURRENT_USER,
                                     r'Software\Microsoft\Windows\CurrentVersion\Uninstall\Google Chrome')
        # print(chrome_key)
    except Exception as e:
        # print(e)
        # print('尚未安装chrome')
        # return None
        try:
            chrome_key = winreg.OpenKey(winreg.HKEY_CURRENT_USER,r'Software\Google\Chrome\BLBeacon')
        except OSError as e:
            # print(e)
            raise OSError('未检测到google安装程序')

    val, t = winreg.QueryValueEx(chrome_key, r'version')
    # print(val)
    return val


def check_driver_exist(python_dir, browser_type):
    '''
    检测python_dir下，浏览器browser_type对应的driver是否已经安装
    :param python_dir: python安装路径，将driver安装在其下
    :param browser_type: 只支持ff和chrome
    :return: boolean。 driver是否存在
    '''
    if browser_type == zw_enum.BrowserType.FireFox:
        file_name = 'geckodriver.exe'
    if browser_type == zw_enum.BrowserType.Chrome:
        file_name = 'chromedriver.exe'

    file_path = os.path.join(python_dir, file_name)
    return os.path.exists(file_path)


def unzip_file(file_path, save_path):
    '''

    :param file_path:待解压的文件
    :param save_path: 解压到的目录
    :return:
    '''
    # 解压zip文件
    f = zipfile.ZipFile(file_path, 'r')
    for file in f.namelist():
        f.extract(file, save_path)
    f.close()

def is_valida_zip_file(file_path):
    return zipfile.is_zipfile(file_path)

if __name__ == '__main__':
    # unzip_file(file_path=r'C:\Python38\geckodriver-v0.26.0-win64.zip', save_path=r'C:\Python38')
    # print(is_valida_zip_file(r'C:\Python38\geckodriver-v0.26.0-win64.zip'))
    get_chrome_version()
