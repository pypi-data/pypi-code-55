#! /usr/bin/env python3
# -*- coding:utf-8 -*-
'''
CpuBits: bits64/bits32
OsType: Windows/Linux
WindowsVersion: Windows7/Windows8/Windows10/Unknown
WindowsBits: Win32/Win64
PythonVersion: Python2/Python3/Unknown
ProxyType: Transparent/Anonymous/High_anonymous
BrowserType: FireFox/Chrome/All
'''
from enum import Enum, unique


@unique
class VariantType(Enum):
    Str = 'str'
    Int = 'int'
    Bool = 'bool'
    Set = 'set'
    List = 'list'
    Tuple = 'tuple'
    Dict = 'dict'



@unique
class CpuBits(Enum):
    bits64 = 0
    bits32 = 1


@unique
class OsType(Enum):
    Windows = 0
    Linux = 1


@unique
class WindowsVersion(Enum):
    Windows7 = 0
    Windows8 = 1
    Windows10 = 2
    Unknown = 3


@unique
class WindowsBits(Enum):
    Win32 = 0
    Win64 = 1

@unique
class PythonVersion(Enum):
    Python2 = 0
    Python3 = 1
    Unknown = 2

@unique
class ProxyType(Enum):
    # 透明：对方服务器知道你使用了代理，也知道你的真实IP。
    # REMOTE_ADDR = ProxyIP，HTTP_VIA = ProxyIP，HTTP_X_FORWARDED_FOR = YourIP
    Transparent = 0
    # 匿名：对方服务器知道你使用了代理，但不知道你的真实IP。
    # REMOTE_ADDR = ProxyIP，HTTP_VIA = ProxyIP，HTTP_X_FORWARDED_FOR = ProxyIP
    Anonymous = 1
    # 高匿名：对方服务器不知道你使用了代理，也不知道你的真实IP。
    # REMOTE_ADDR = ProxyIP，HTTP_VIA = NULL，HTTP_X_FORWARDED_FOR = NULL
    High_anonymous = 2
    All = 3



@unique
class BrowserType(Enum):
    FireFox = 0
    Chrome = 1
    All = 2

