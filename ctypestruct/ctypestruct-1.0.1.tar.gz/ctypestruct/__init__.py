
#!/usr/bin/env python
# coding: utf-8

import copy,binascii

"""小端存储，字节反转"""

def rever_bytes(str_buf):
    assert (len(str_buf) % 2 == 0)
    return str(binascii.hexlify(binascii.unhexlify(str_buf)[::-1]),encoding = "utf-8")



"""按byte读取数据"""

def app_bitmap_read_byte(pstr, struct_c, reverse = True):
    struct_dict = copy.copy(struct_c) # 浅拷贝，不修改内部数据
    bit_list = list(struct_dict.values())
    index = 0
    for i in range(len(bit_list)):
        if reverse:
            bit_result = eval("0x" + (rever_bytes(pstr[index:index + int(bit_list[i] * 2)])))
        else:
            bit_result = eval("0x" + (pstr[index:index + int(bit_list[i] * 2)]))

        struct_dict[list(struct_dict.keys())[i]] = bit_result
        #str_list.append(bit_result)
        index += int(bit_list[i] * 2)
    
    class struct_data(object):  # 最小类：类似c语言结构体
        def __init__(self):
            names = self.__dict__
            for key,value in struct_dict.items(): # 动态赋值变量
                names[key] = value
    return  struct_data()



"""按bit读取数据"""
def app_bitmap_read_bit(pstr, struct_c, reverse = True):
    struct_dict = copy.copy(struct_c) # 浅拷贝，不修改内部数据
    bit_list = list(struct_dict.values())
    index = -bit_list[0]
    del bit_list[0]
    if reverse:
        pstr = str(bin(int("1" + rever_bytes(pstr), 16))).split("0b1")[1]
    else:
        pstr = str(bin(int("1" + pstr, 16))).split("0b1")[1]

    pstr = str(bin(int("1" + rever_bytes(pstr), 16))).split("0b1")[1]
    struct_dict[list(struct_dict.keys())[0]] = int((eval("0b" + pstr[index:])))
    for i in range(len(bit_list)):
        bit_result = int((eval("0b" + pstr[-(-index + bit_list[i]):index]))) # 反向获取数据
        struct_dict[list(struct_dict.keys())[i+1]] = bit_result
        index += -bit_list[i]

    class struct_data(object):  # 最小类：类似c语言结构体
        def __init__(self):
            names = self.__dict__
            for key,value in struct_dict.items(): # 动态赋值变量
                names[key] = value
    return  struct_data()