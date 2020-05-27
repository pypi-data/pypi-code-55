"""
@File    :   GenTestData.py    
@Contact :   zhangkun0518@outlook.com
@Software:   PyCharm
@Modify Time      @Author    @Version    @Desciption
------------      -------    --------    -----------
2020/5/12 17:47  kun.z      1.0         None
"""
import re
import datetime
import random
import string
class GenTestData():
    """
    随机生成字符串
    """
    def gen_test_data_str(self,data_type: str):
        data_type_lit = data_type.split('+')
        str_ret = ''
        p1 = re.compile(r'[(](.*?)[)]', re.S)
        for each in data_type_lit:
            if 'datetime' in each:
                tmp = re.findall(p1, each)
                day_random = random.randint(1,100)
                second_random = random.randint(1,10000)
                if not tmp:
                    tmp = ['%Y-%m-%d %H:%M:%S']
                str_ret = str_ret + (datetime.datetime.now() - datetime.timedelta(days=day_random,seconds=second_random)).strftime(tmp[0])
            elif 'int' in each:
                data_len = 5
                tmp = re.findall(p1, each)
                if tmp:
                    data_len = int(tmp[0])
                num_int = random.randint(pow(10,(data_len-1)),pow(10,(data_len-0)) )
                str_ret = str_ret + str( num_int )

            elif 'float' in each:
                int_len = 5
                decimal_len = 5
                tmp = re.findall(p1, each)
                if tmp:
                    tmp_list = tmp[0].split('.')
                    int_len = int(tmp_list[0])
                    if len(tmp_list)>1:
                        decimal_len = int(tmp_list[0])
                num_int = random.randint(pow(10,(int_len-1)),pow(10,(int_len-0)) )
                num_decimal = random.randint(pow(10,(decimal_len-1)),pow(10,(decimal_len-0)) )
                str_ret = str_ret + str( num_int ) + '.' + str(num_decimal)
            elif 'str' in each:
                data_len = 5
                tmp = re.findall(p1, each)
                if tmp:
                    data_len = int(tmp[0])
                for i in range(0,data_len):
                   str_ret = str_ret + random.choice(string.ascii_letters)
    
        return str_ret
        
gem_test_data = GenTestData()
def mytest():
    tmp = GenTestData()
    data1 = 'int(8)'
    print(tmp.gen_test_data_str(data1))
    data1 = 'float(4.4)'
    print(tmp.gen_test_data_str(data1))
    data1 = 'str(8)'
    print(tmp.gen_test_data_str(data1))
    data1 = 'datetime(%Y-%m-%d %H:%M:%S)'
    print(tmp.gen_test_data_str(data1))
    data1 = 'str(3)+int(4)'
    print(tmp.gen_test_data_str(data1))
if __name__=='__main__':
    mytest()