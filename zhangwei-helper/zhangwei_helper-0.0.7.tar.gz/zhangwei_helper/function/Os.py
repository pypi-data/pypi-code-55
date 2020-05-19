#! /usr/bin/env python3
# -*- coding:utf-8 -*-
'''
get_cpu_bits(): 枚举(CpuBits)：cpu的位数
get_os_type(): 枚举(OsType)：os的类型：windows或者linux
get_windows_ver(): 枚举(WindowsVersion)：windows的版本（7/8/10）
get_windows_bits(): 枚举(WindowsBits)：windows的位数：32或者64
windows_login_as_admin(): Boolean：当前是否以admin登录
get_python_major_version():枚举(PythonVersion)：返回python的大版本号：2或者3或者unknown
'''
import sys
import os
import platform
import ctypes
import zhangwei_helper.enum.SelfEnum as self_enum


def get_cpu_bits():
    '''
    CPU的位数，是32bit，还是64bit
    :return:
    '''
    if os.environ.get('PROCESSOR_ARCHITECTURE') == 'AMD64':
        return self_enum.CpuBits.bits64
    else:
        return self_enum.CpuBits.bits32


def get_os_type():
    '''
    操作系统的类型，是win还是linux
    :return:
    '''
    if platform.system() == 'Windows':
        return self_enum.OsType.Windows
    if platform.system() == 'Linux':
        return self_enum.OsType.Linux


def get_windows_ver():
    '''
    windows的版本
    :return:
    '''
    ver = platform.platform().split('-')[1:2:1][0]

    if ver == '7':
        return self_enum.WindowsVersion.Windows7
    elif ver == '8':
        return self_enum.WindowsVersion.Windows8
    elif ver == '10':
        return self_enum.WindowsVersion.Windows10
    else:
        return self_enum.WindowsVersion.Unknown


def get_windows_bits():
    '''
    windows的位数
    :return:
    '''
    if 'PROGRAMFILES(X86)' in os.environ:
        return self_enum.WindowsBits.Win64
    else:
        return self_enum.WindowsBits.Win32


def windows_login_as_admin():
    if get_os_type() == self_enum.OsType.Windows:
        return ctypes.windll.shell32.IsUserAnAdmin() != 0


def get_python_major_version():
    major_version = sys.version_info[0]
    if major_version == 2:
        return self_enum.PythonVersion.Python2
    elif major_version == 3:
        return self_enum.PythonVersion.Python3
    else:
        return self_enum.PythonVersion.Unknown
# print(windows_login_as_admin())