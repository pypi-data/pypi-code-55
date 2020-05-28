# -*- coding: utf-8 -*-
import ctypes
import os
import sys
from ctypes import *
from iqsopenapi.trade.realtrade.TradeEnums import TradeCounterType
from iqsopenapi.trade.realtrade.Models import kv

class SupervisionHelper:
    def __init__(self):

        if self.__isLinux():
            self.__libpath = os.path.join(os.path.dirname(__file__), 'linux')
        else:
            if self.__isX64():
                self.__libpath = os.path.join(os.path.dirname(__file__), 'win','x64')
            else:
                self.__libpath = os.path.join(os.path.dirname(__file__), 'win','x86')
        os.chdir(self.__libpath)

    def string_buffer2string(self, buffer, length, code='ascii'):
        return buffer.value[:length].decode(code).strip()
        
    def create_string_buffer(self, length):
        return ctypes.create_string_buffer(length)

    def dingdian(self):
        dingdian = cdll.LoadLibrary('InformationCollect.dll')
        length = 1024
        infoSb = self.create_string_buffer(length)
        cryptVerSb = self.create_string_buffer(length)
        result= dingdian.apexsoft_getsysteminfo(infoSb, length, cryptVerSb, length)
        info = self.string_buffer2string(infoSb, length)
        crypt = self.string_buffer2string(cryptVerSb, length)
        return result, info, crypt
        
    def ctp(self):
        length = 1024
        array = (c_byte * length)()
        len = (c_int*1)()
        if self.__isLinux():
            func_name = '_Z21CTP_GetRealSystemInfoPcRi'
            absolute_dllfile_path = os.path.join(self.__libpath, 'LinuxDataCollect.so')
            ctp = CDLL(absolute_dllfile_path)
        else:
            ctp = CDLL('WinDataCollect.dll')
            if self.__isX64():
                func_name = '?CTP_GetSystemInfo@@YAHPEADAEAH@Z'
            else:
                func_name = '?CTP_GetSystemInfo@@YAHPADAAH@Z'
        result = ctp[func_name](array, len)
        temp_list = array[:len[0]]
        info = ','.join(list(map(str, temp_list)))
        return result, info
        
    def hundsun(self):
        #stdcall约定用windll加载
        hs = windll.LoadLibrary('HsFutuSystemInfo.dll')
        length = 1024
        infoSb = self.create_string_buffer(length)
        integritySb = self.create_string_buffer(length)
        infoLength = (c_int*1)(length)
        integrityLength = (c_int*1)(length)
        result = hs.hundsun_getsysteminfo(infoSb, infoLength, integritySb, integrityLength)
        info = self.string_buffer2string(infoSb, infoLength[0])
        integrity = self.string_buffer2string(integritySb, integrityLength[0])
        return result, info, integrity
        
    def jsd(self):
        jsd = cdll.LoadLibrary('KCC_API.dll')
        length = 1024
        infoSb = self.create_string_buffer(length)
        infoLength = (c_int*1)(length)
        result = jsd.KingStar_GetSystemInfo(infoSb, infoLength)
        if(result != 0): raise Exception('获取JSD穿透式监管信息时出错')
        info = self.string_buffer2string(infoSb, infoLength[0])
        return result, info
        
    def fm(self):
        fm = cdll.LoadLibrary('FMCollectWrapper.dll')
        length = 1024
        infoSb = self.create_string_buffer(length)
        infoLength = (c_int*1)(length)
        flagPoint = (c_int*1)()
        result = fm.StaticGetUserLocalSystemInfo(infoSb, length, infoLength, flagPoint)
        if(result != 0): raise Exception('获取FM穿透式监管信息时出错')
        info = self.string_buffer2string(infoSb, infoLength[0])
        return result, info, flagPoint[0]

    def SetInfo(self, supInfo):
        info = ''
        integrity = ''
        ver = ''
        except_code = 0
        json = []
        if (supInfo.TradeCounter == TradeCounterType.CTP):
            except_code, info = self.ctp()
            json.append(kv('sysInfo', info))
            json.append(kv('exceptionType', except_code))
        elif (supInfo.TradeCounter == TradeCounterType.HS):
            except_code, info, integrity = self.hundsun()
            json.append(kv('sysInfo', info))
            json.append(kv('sysInfoIntegrity', integrity))
            json.append(kv('exceptionType', except_code))
        elif (supInfo.TradeCounter == TradeCounterType.DD):
            except_code, info, ver = self.dingdian()
            json.append(kv('sysInfo', info))
            json.append(kv('encrypKeyVersion', ver))
            json.append(kv('exceptionType', except_code))
        elif (supInfo.TradeCounter == TradeCounterType.JSD):
            except_code, info= self.jsd()
            json.append(kv('sysInfo', info))
            json.append(kv('exceptionType', except_code))
        elif (supInfo.TradeCounter == TradeCounterType.FM):
            except_code, info, flag= self.fm()
            json.append(kv('sysInfo', info))
            json.append(kv('exceptionType', except_code))
        else : raise Exception('不支持的穿透式监管类型!')
        supInfo.SysInfo = info
        supInfo.EncrypKeyVersion = ver
        supInfo.SysInfoIntegrity = integrity
        supInfo.ExceptionType = str(except_code)
        return json

    def __isX64(self):
        return sys.maxsize > 2**32

    def __isLinux(self):
        return sys.platform == "linux" or sys.platform == "linux2"

if __name__ == '__main__':
    #Supervision文件夹放到此文件目录下
    helper = SupervisionHelper()
    
    #dingdian
    print('dingdian')
    result,info,crypt = helper.dingdian()
    print(f'info:{info}\ncrypt:{crypt}\nresult:{result}')

    #ctp
    print('\n\nctp')
    result,info = helper.ctp()
    print(f'info:{info}\nresult:{result}')

    #hundsun
    print('\n\nhundsun')
    result,info,integrity = helper.hundsun()
    print(f'info:{info}\nintegrity:{integrity}\nresult:{result}')

    #jsd
    print('\n\njsd')
    result,info = helper.jsd()
    print(f'info:{info}\nresult:{result}')

    #fm
    print('\n\nfm')
    result,info,flag = helper.fm()
    print(f'info:{info}\nflag:{flag}\nresult:{result}')