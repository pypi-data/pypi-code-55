# -*- coding:utf-8 -*-
'''
对变量类型进行检查
match_expect_type(value, expect_type): Boolean。是否为匹配的类型
all_values_preDefined_enum(values, defined_enum):boolean。values中所有值都是预定义的enum中的一员
enum_set_check(value, enum_type, replace=True): 1. 是否为set 2. set中每个值是否为enum中的一员
    3. 如果set中有ALL，且replace=True，用除了ALL之外的其他所有成员替代All。返回None（有错误），或者原始
    值（或者替换后的值）
check_if_ipv4(value)：Boolean。检测输入的是否为合格的ipv4
check_if_ipv4_port(value)：Boolean。检测输入的是否为合格的ipv4的port

'''

import zhangwei_helper.enum.SelfEnum as self_enum


def match_expect_type(value, expect_type):
    '''
    :param value:  待检查的值
    :param expect_type:enum(VariantEnum)    期望的类型
    :return: Boolean
    '''
    return expect_type.value in str(type(value))


def all_values_pre_defined_enum(values, defined_enum):
    '''
    判断values里的值，是否都是预定义的enum
    :param values: list/set/tuple
    :param defined_enum: 自定义的enum
    :return: boolean，true：values中所有值都是预定义的，false：有非预定义的值
    '''

    def filter_func(value):
        # defined_enum.__name__  ==> enum的名字，例如OsType
        # str(type(value))       ==> 变量的类型，如果是OsType的enum，则是<enum 'OsType'>
        return '' if defined_enum.__name__ in str(type(value)) else 'False'

    r = set(filter(filter_func, values))
    # print(r)
    return len(r) == 0


def enum_set_check(value, enum_type, replace=True):
    '''
    检测value是否为set（防止重复），且其中每个值都是enum_type中成员，最后，如果有value中有all，替换所有其他成员
    :param value: 待检查的值
    :param enum_type: enum的定义
    :param replace: boolean，当value为True，是否用enum中其他所有值取代All
    :return: None（有错误）/set（原始值，或者修改过的值（All））
    '''
    # value是set
    if not match_expect_type(value, self_enum.VariantType.Set):
        # print('not set')
        return
    # value中每个值是合法的enum成员
    if not all_values_pre_defined_enum(values=value, defined_enum=enum_type):
        # print('not valid')
        return
    # value中有all，则把除all之外的成员都设置上去
    # print(enum_type['All'] in value)
    if enum_type['All'] in value:
        # print(enum_type.__members__.items())
        if replace:
            return set(
                [enum_type[k] for k, v in enum_type.__members__.items() if
                 k != 'All'])
        else:
            return {enum_type['All']}
    else:
        return value


def check_if_ipv4(value):
    '''
    检测输入的是否为IP：1. 字符串  2. 分割后为4个元素  3. 每个元素必须的长度1～3 4.每个元素可以转换成数字，且数字位于0到255
    :param value:
    :return: Boollean
    '''
    if not match_expect_type(value, self_enum.VariantType.Str):
        return False

    tmp = value.split('.')
    if len(tmp) != 4:
        return False

    for tmp_ele in tmp:
        length = len(tmp_ele)
        if length == 0 or length > 3:
            return False

        try:
            convert_tmp_ele = int(tmp_ele)
        except ValueError as e:
            return False

        if convert_tmp_ele<0 or convert_tmp_ele > 255:
            return False

    return True

def check_if_ipv4_port(value):
    '''
    检测是否合格的port： 1.是str 2 可以转换成数字，且在0到65535之间
    :param value:
    :return: Boolean
    '''
    if not match_expect_type(value, self_enum.VariantType.Str):
        return False

    try:
        convert_value = int(value)
    except ValueError as e:
        return False

    if convert_value < 0 or convert_value >65535:
        return False

    return True
