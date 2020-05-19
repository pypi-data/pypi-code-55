'''
对windows的注册表进行操作
_open_key: 返回key
_read_key_value：读取key下一个value的值和类型
_save_key_value：以某种类型的方式，把值保存到某个key中

read_PATH_value：读取环境变量PATH的值
append_value_in_PATH：为PATH添加一个值
del_value_in_PATH：从PATH中删除一个值
check_key_value_exists(key,value_name)：检查某个key小，value_name是否存在
create_value(key,value_name,value_type,value): 直接调用_save_key_value
delete_value(key,value_name): 删除key下的value
'''

import winreg


def _open_key(root_key_name,sub_key_name):
    try:
        key = winreg.OpenKey(root_key_name, sub_key_name,0 ,winreg.KEY_ALL_ACCESS)
    except Exception as e:
        if root_key_name == winreg.HKEY_CURRENT_USER:
            root_key_name = 'HKEY_CURRENT_USER'
        elif root_key_name == winreg.HKEY_CLASSES_ROOT:
            root_key_name = 'HKEY_CLASSES_ROOT'
        elif root_key_name == winreg.HKEY_CURRENT_CONFIG:
            root_key_name = 'HKEY_CURRENT_CONFIG'
        elif root_key_name == winreg.HKEY_DYN_DATA:
            root_key_name = 'HKEY_DYN_DATA'
        elif root_key_name == winreg.HKEY_LOCAL_MACHINE:
            root_key_name = 'HKEY_LOCAL_MACHINE'
        elif root_key_name == winreg.HKEY_PERFORMANCE_DATA:
            root_key_name = 'HKEY_PERFORMANCE_DATA'
        elif root_key_name == winreg.HKEY_USERS:
            root_key_name = 'HKEY_USERS'
        raise EnvironmentError('注册表的项%s\%s不存在' % (root_key_name,sub_key_name))
    return key
    # val, tpe = winreg.QueryValueEx(sub_item, key_name)


def _read_key_value(key,value_name):
    val, tpe = winreg.QueryValueEx(key, value_name)
    return val,tpe

def _save_key_value(key,value_name,value_type,value):
    # key = winreg.OpenKey(sub_item,key_name)
    # v,t = _read_key_value(sub_item,key_name)
    winreg.SetValueEx(key,value_name, 0, value_type, value)

def check_key_value_exists(key,value_name):
    # key = _open_key(winreg.HKEY_CURRENT_USER, r'Environment')
    sub_key_num, value_num, last_modified = winreg.QueryInfoKey(key)
    # print(winreg.EnumValue(sub_item, 2))
    # winreg.EnumKey(sub_item, 1)
    # print(list(range(0,key_num)))
    if value_num > 0:
        for idx in list(range(0, value_num)):
            tmp_val_name, tmp_val, idx = winreg.EnumValue(key, idx)
            if tmp_val_name.lower() == value_name.lower():
                return True
    return False

def create_value(key,value_name,value_type,value):
    _save_key_value(key,value_name,value_type,value)

def delete_value(key,value_name):
    winreg.DeleteValue(key,value_name)

def read_PATH_value():
    '''
    读取windown环境变量PATH的内容
    :return:
    '''
    root_key = winreg.HKEY_CURRENT_USER
    sub_key_name = r'Environment'
    value_name = r'PATH'
    key = _open_key(root_key, sub_key_name)
    val, tpe = _read_key_value(key, value_name)
    return val,tpe
    # print(val)

def append_value_in_PATH(v):
    '''
    把v添加到系统变量PATH中去
    :param v:
    :return:
    '''
    root_key = winreg.HKEY_CURRENT_USER
    sub_key_name = r'Environment'
    value_name = r'PATH'
    key = _open_key(root_key, sub_key_name)
    val, tpe = _read_key_value(key,value_name)
    #检测是否包含
    tmp = val.split(';')
    if v not in tmp:
        _save_key_value(key, value_name, tpe,val+';'+v)

    winreg.CloseKey(key)

def del_value_in_PATH(v):
    '''
    把v添加到系统变量PATH中去
    :param v:
    :return:
    '''
    root_key = winreg.HKEY_CURRENT_USER
    sub_key_name = r'Environment'
    value_name = r'PATH'
    key = _open_key(root_key, sub_key_name)
    val, tpe = _read_key_value(key,value_name)

    tmp = val.split(';')
    tmp.remove(v)
    _save_key_value(key, value_name, tpe,';'.join(tmp))

    winreg.CloseKey(key)

# key = _open_key(winreg.HKEY_CURRENT_USER, r'Environment')
# delete_value(key, 'test')