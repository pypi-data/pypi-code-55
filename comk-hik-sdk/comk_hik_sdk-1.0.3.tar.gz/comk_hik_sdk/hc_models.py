from ctypes import *


# 日期结构体
class NET_DVR_TIME_EX(Structure):
    _fields_ = [
        ('wYear', c_ushort),
        ('byMonth', c_ubyte),
        ('byDay', c_ubyte),
        ('byHour', c_ubyte),
        ('byMinute', c_ubyte),
        ('bySecond', c_ubyte),
        ('byRes', c_ubyte),
    ]


LPNET_DVR_TIME_EX = POINTER(NET_DVR_TIME_EX)


# 有效期参数结构体
class NET_DVR_VALID_PERIOD_CFG(Structure):
    _fields_ = [
        ('byEnable', c_ubyte),
        ('byBeginTimeFlag', c_ubyte),
        ('byEnableTimeFlag', c_ubyte),
        ('byTimeDurationNo', c_ubyte),
        ('struBeginTime', NET_DVR_TIME_EX),
        ('struEndTime', NET_DVR_TIME_EX),
        ('byTimeType', c_ubyte),
        ('byRes2', c_ubyte * 31),
    ]


LPNET_DVR_VALID_PERIOD_CFG = POINTER(NET_DVR_VALID_PERIOD_CFG)


# 定义组件库加载路径信息结构体
class NET_DVR_LOCAL_SDK_PATH(Structure):
    _fields_ = [
        ('sPath', c_char * 256),
        ('byRes', c_ubyte * 128),
    ]


# 用户信息结构体 -- NET_DVR_USER_LOGIN_INFO
class NET_DVR_USER_LOGIN_INFO(Structure):
    _fields_ = [
        ('sDeviceAddress', c_ubyte * 129),
        ('byUseTransport', c_ubyte),
        ('wPort', c_short),
        ('sUserName', c_ubyte * 64),
        ('sPassword', c_ubyte * 64),
        ('cbLoginResult', c_void_p),
        ('pUser', c_void_p),
        ('bUseAsynLogin', c_int),
        # ('byProxyType', c_ubyte),
        # ('byUseUTCTime', c_ubyte),
        # ('byLoginMode', c_ubyte),
        # ('byHttps', c_ubyte),
        # ('iProxyID', c_ubyte),
        # ('byVerifyMode', c_ubyte),
        ('byRes2', c_ubyte * 128),
        # ('byRes3', c_ubyte * 128),
    ]


# LPNET_DVR_USER_LOGIN_INFO = POINTER(NET_DVR_USER_LOGIN_INFO)


# 登录设备结构体 -- NET_DVR_DEVICEINFO_V30
class NET_DVR_DEVICEINFO_V30(Structure):
    _fields_ = [
        ('sSerialNumber', c_ubyte * 48),
        ('byAlarmInPortNum', c_ubyte),
        ('byAlarmOutPortNum', c_ubyte),
        ('byDiskNum', c_ubyte),
        ('byDVRType', c_ubyte),
        ('byChanNum', c_ubyte),
        ('byStartChan', c_ubyte),
        ('byAudioChanNum', c_ubyte),
        ('byIPChanNum', c_ubyte),
        ('byZeroChanNum', c_ubyte),
        ('byMainProto', c_ubyte),
        ('bySubProto', c_ubyte),
        ('bySupport', c_ubyte),
        ('bySupport1', c_ubyte),
        ('bySupport2', c_ubyte),
        ('wDevType', c_ushort),
        ('bySupport3', c_ubyte),
        ('byMultiStreamProto', c_ubyte),
        ('byStartDChan', c_ubyte),
        ('byStartDTalkChan', c_ubyte),
        ('byHighDChanNum', c_ubyte),
        ('bySupport4', c_ubyte),
        ('byLanguageType', c_ubyte),
        ('byVoiceInChanNum', c_ubyte),
        ('byStartVoiceInChanNo', c_ubyte),
        ('bySupport5', c_ubyte),
        ('bySupport6', c_ubyte),
        ('byMirrorChanNum', c_ubyte),
        ('wStartMirrorChanNo', c_ushort),
        ('bySupport7', c_ubyte),
        ('byRes2', c_ubyte),
    ]


# LPNET_DVR_DEVICEINFO_V30 = POINTER(NET_DVR_DEVICEINFO_V30)


# 登录设备结构体 -- NET_DVR_DEVICEINFO_V40
class NET_DVR_DEVICEINFO_V40(Structure):
    _fields_ = [
        ('struDeviceV30', NET_DVR_DEVICEINFO_V30),
        ('bySupportLock', c_ubyte),
        ('byRetryLoginTime', c_ubyte),
        ('byPasswordLevel', c_ubyte),
        ('byRes1', c_ubyte),
        ('dwSurplusLockTime', c_short),
        ('byLoginMode', c_ubyte),
        ('iResidualValidity', c_uint),
        ('byRes2', c_ubyte * 256),
    ]


# LPNET_DVR_DEVICEINFO_V40 = POINTER(NET_DVR_DEVICEINFO_V40)


# 卡参数配置条件结构体
class NET_DVR_CARD_COND(Structure):
    _fields_ = [
        ('dwSize', c_uint),
        ('dwCardNum', c_uint),
        ('byRes', c_ubyte * 64),
    ]


# 卡数据记录结构体，与 NET_DVR_CARD_COND 匹配使用
class NET_DVR_CARD_RECORD(Structure):
    _fields_ = [
        ('dwSize', c_uint),
        ('byCardNo', c_ubyte * 32),
        ('byCardType', c_ubyte),
        ('byLeaderCard', c_ubyte),
        ('byUserType', c_ubyte),
        ('byRes1', c_ubyte),
        ('byDoorRight', c_ubyte * 256),
        ('struValid', NET_DVR_VALID_PERIOD_CFG),
        ('byBelongGroup', c_ubyte * 128),
        ('byCardPassword', c_ubyte * 8),
        ('wCardRightPlan', c_short * 256),
        ('dwMaxSwipeTimes', c_uint),
        ('dwSwipeTimes', c_uint),
        ('dwEmployeeNo', c_uint),
        ('byName', c_ubyte * 32),
        ('dwCardRight', c_uint),
        ('byRes', c_ubyte * 256),
    ]


LPNET_DVR_CARD_RECORD = POINTER(NET_DVR_CARD_RECORD)


# 获取卡信息，与 NET_DVR_CARD_COND 匹配使用
class NET_DVR_CARD_SEND_DATA(Structure):
    _fields_ = [
        ('dwSize', c_int),
        ('byCardNo', c_ubyte * 32),
        ('byRes', c_ubyte * 16),
    ]


class NET_DVR_CARD_STATUS(Structure):
    _fields_ = [
        ('dwSize', c_uint),
        ('byCardNo', c_ubyte * 32),
        ('dwErrorCode', c_uint),
        ('byStatus', c_ubyte),
        ('byRes', c_ubyte * 23),
    ]
