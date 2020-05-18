"""
    因为kw618的init中只能导入全局变量/函数/类, 而无法导入类中的函数.
    所以, 其实把该模块作为一个"大的类", 里面都是类中实现某些功能的函数
    所以, docs_2_df 函数, 其实没必要归纳到类中. 这样显得层级很复杂, 而且也不方便外部脚本调用该函数.
"""
import pandas as pd
import numpy as np
import math
import collections
import pymongo
import json
import copy

import warnings
warnings.filterwarnings("ignore")

# 导入常用的固定路径(多平台通用)
from kw618._file_path import *

def import_data(
    in_file_name="in", end_index=None, field=None, is_df=True,
    in_file_path=None, encoding="gb18030", index_col=None,
    ):
    """
    in:csv文件
    out:df类型/类mongo类型
    function:  csv → df/mongo (默认转出:类mongo)

    notes: in_file_path 的优先级比 in_file_name 高。

    ttt:0214
    """
    if in_file_path:
        df = pd.read_csv(in_file_path, encoding=encoding, engine='python', index_col=index_col)
    else:
        df = pd.read_csv(FILE_PATH_FOR_DESKTOP+"/{0}.csv".format(in_file_name), encoding=encoding, engine='python', index_col=index_col)
    if is_df:
        return df
    # 1.需要返回的是某个字段的lst格式
    if field:
        field_lst = df[field].values[:end_index] # 得到的是np.array格式
        return list(field_lst) # 用list数据格式来返回
    # 2.返回的是mongo支持的docs
    df = df[:end_index]
    docs = df.T.to_dict().values()
    return docs



    #  也可以用于 "mongo → df"
def output_data(
    in_obj, out_file_name="out", ordered_field_lst=None,
    out_file_path=None, output=True, index=False, encoding="gb18030", export_excel=False,
    ):
    """
    in:类mongo/df
    out:csv文件
    function:  1.mongo/df  → csv
               2.mongo → df (这样output设为False即可)

    in_obj:    不管是mongo还是df,自动先转化成df,再用它来转csv

    tips: 如果需要 "mongo → df": output设置为False即可!
    notes: out_file_path 的优先级比 out_file_name 高。

    """

    # 1. 如果不是df类型,先将类mongo的数据,转化成df
    if isinstance(in_obj, pymongo.cursor.Cursor):
        # total_items = []
        # for doc in in_obj:
        #     # items = {i:str(j).strip() for i, j in zip(list(doc.keys()), list(doc.values()))}
        #     # 以下会按照mongo中存着的顺序进行输出!
        #     items = collections.OrderedDict({i:str(j).strip() for i, j in zip(list(doc.keys()), list(doc.values()))})
        #     total_items.append(items)
        # df = pd.DataFrame(total_items)
        df = pd.DataFrame(list(in_obj))  # 如果in_obj的数据量是上百万条, 其实这个操作很危险的!!
    elif isinstance(in_obj, pd.core.frame.DataFrame):
        df = in_obj

    # 2.确定字段的呈现顺序
    if ordered_field_lst:
        # 如果指定的df字段在df中并不存在,则把该字段remove掉.确保不报错
        for field in ordered_field_lst.copy():
            if field not in df.columns:
                print("字段 {} 不在df中,将其抛弃!".format(field))
                ordered_field_lst.remove(field)
        df = df[ordered_field_lst]  # 指定顺序

    # 3.看是否需要导出csv文件,如果不需要,直接返回df
    if not output:
        return df

    # 4. 最后,将df数据转成csv文件输出
    try:
        if out_file_path:
            if not export_excel:
                df.to_csv(out_file_path, index=index, encoding=encoding)
            else:
                df.to_excel(out_file_path, index=index, encoding=encoding)
        else:
            if not export_excel:
                df.to_csv(FILE_PATH_FOR_DESKTOP+"/{0}.csv".format(out_file_name), index=index, encoding=encoding)
            else:
                df.to_excel(FILE_PATH_FOR_DESKTOP+"/{0}.xlsx".format(out_file_name), index=index, encoding=encoding)
    except Exception as e:
        print(e)
        out_file_name = input("输出文件名出错,请重新键入文件名: ")
        df.to_csv(FILE_PATH_FOR_DESKTOP+"/{0}.csv".format(out_file_name), index=index, encoding=encoding)

    return df


# class KwPd():
#     def __init__(self):
#         pass
#
#     def docs_2_df(self, docs, ordered_field_lst=None):
#         """
#         把mongo的数据转化成df
#         """
#         df = output_data(docs, output=False, ordered_field_lst=ordered_field_lst)
#         return df



def docs_to_df(docs, ordered_field_lst=None):
    """
    把mongo的数据转化成df
    """
    df = output_data(docs, output=False, ordered_field_lst=ordered_field_lst)
    return df


def df_2_mongo(df):
    return df.T.to_dict().values() # 即：docs
def df_to_docs(df, is_lst=False):
    if is_lst:
        return list(df.T.to_dict().values())
    else:
        return df.T.to_dict().values() # 即：docs


def read_excel(in_file_name="in", in_file_path=None, sheet_name=None):
    """
    sheet_name:
        不传参数:[默认为0] 表示取第一个sheet作为df的数据, 返回df类型
        传入None: 返回一个有序字典 OrderedDict([("<sheet名字>", <df对象>)])
                ( 需要用sheet名来按键取值)
        [这里, 我一律传入None, 方便后续合并多个sheet]
    """
    if in_file_path is not None:
        ordered_d = pd.read_excel(in_file_path, sheet_name=None)
    elif in_file_path is None:
        ordered_d = pd.read_excel(f"{FILE_PATH_FOR_DESKTOP}/{in_file_name}.xlsx", sheet_name=None)

    concat_df = pd.concat([sheet for sheet in ordered_d.values()], axis=0, ignore_index=True)

    return concat_df


def sort_df(df, ordered_field_lst):
    # 1. 如果指定的字段在df中并不存在,则把该字段remove掉.确保不报错
    ordered_field_lst_copy = ordered_field_lst.copy()
    for field in ordered_field_lst_copy:
        if field not in df.columns:
            print("字段 {} 不在df中, 将其抛弃!".format(field))
            ordered_field_lst.remove(field)

    # 2. 把所需要保留的 "有序字段list" 作用在df上
    return df[ordered_field_lst]  # 指定顺序




# stackoverflow 白嫖来的函数，hhh
def read_mongo(collection_obj, query={}, need_to_show_dict={"_id":0}, df_name="foo"):
    """ Read from Mongo and Store into DataFrame """


    # Make a query to the specific DB and Collection
    cursor = collection_obj.find(query, need_to_show_dict)

    # Expand the cursor and construct the DataFrame
    df =  pd.DataFrame(list(cursor))

    df.df_name = df_name


    if "crawl_date" in df.columns:
        df["crawl_date"] = pd.to_datetime(df["crawl_date"])
    if "date" in df.columns:
        df["date"] = pd.to_datetime(df["date"])

    return df





def date_to_obj(date_str="today"):
    return pd.to_datetime(date_str)

def obj_to_date(date_obj, format_="%Y-%m-%d"):
    return date_obj.strftime(format_)

def get_today_obj(date_str="today"):
    return pd.to_datetime(date_str)

def get_days(days_str="1 d"):
    "1天的时间段"
    return pd.to_timedelta(days_str)

def get_this_time():
    "此刻的时间"
    today_obj = pd.to_datetime("today")
    return today_obj.strftime("%X") # 转成“15:43:36”这样的str形式


def get_today_date(date_str="today", format_="%Y-%m-%d"):
    "今天的日期"
    today_obj = pd.to_datetime(date_str)
    return today_obj.strftime(format_) # 转成“2019-02-28”这样的str形式
# 简化版的当前日期
def get_sim_today_date():
    return get_today_date(format_="%m%d") # 转成“0228”这样的str形式
# 简化版的昨天日期
def get_sim_yesterday_date():
    return get_yesterday_date(format_="%m%d") # 转成“0228”这样的str形式


def get_yesterday_obj(date_str="today"):
    today_obj = pd.to_datetime(date_str)
    yesterday_obj = today_obj - pd.to_timedelta("1 d")
    return yesterday_obj

def get_yesterday_date(date_str="today", format_="%Y-%m-%d"):
    " 昨天的日期"
    today_obj = pd.to_datetime(date_str)
    yesterday_obj = today_obj - pd.to_timedelta("1 d")
    yesterday_date = yesterday_obj.strftime(format_) # 转成“20190228”这样的str形式
    return yesterday_date

def get_previous_date(date_str="today", days_str="10 d", format_="%Y-%m-%d"):
    today_obj = pd.to_datetime(date_str)
    days_obj = get_days(days_str)
    previous_date_obj = today_obj - days_obj
    previous_date = previous_date_obj.strftime(format_)
    return previous_date




def get_this_month_first_date(date_str="today"):
    " 本月第一天的日期"
    today_obj = get_today_obj(date_str)
    this_month_first_obj = get_today_obj(today_obj.strftime("%Y-%m"))
    this_month_first_date = obj_to_date(this_month_first_obj)
    return this_month_first_date



def get_period_df(start_date=None, end_date=None, is_crawl_date=False):
    " 获取一段时间内的 <日期扩充表> "
    if start_date is None:
        this_month_first_date = get_this_month_first_date()
        start_date = this_month_first_date
    if end_date is None:
        end_date = get_today_date()

    # 两种方式截取 "日期范围"
    datetime_index = pd.date_range(start_date, end_date, freq="1d")
    if is_crawl_date: # 用"crawl_date"来选择 "日期范围"
        df = pd.DataFrame({"crawl_date":datetime_index})
        df["true_date"] = df.crawl_date - get_days("1 d")
    else: # 用"true_date"来选择 "日期范围"
        df = pd.DataFrame({"true_date":datetime_index})
        df["crawl_date"] = df.true_date + get_days("1 d")

    # 生成4中 str格式的日期  (用于后期透视)
    df["日期"] = df.true_date.dt.strftime("%Y-%m-%d")
    df["日期-年"] = df.true_date.dt.strftime("%Y") # series类型正常来说是不能直接strftime成str类型的, 必须要用.dt 方法才行
    df["日期-月"] = df.true_date.dt.strftime("%Y-%m")
    # 计算"日期-周"这个 '周度日期 '
    weekly_date_lst = []
    for count, date_str in enumerate(df["日期"][-1::-1]): # 对'日期'的series逆序
        if count % 7 == 0:
            tmp = date_str
        weekly_date_lst.append(tmp)
    df["日期-周"] = weekly_date_lst[-1::-1] # 上面逆序了, 现在逆序回来
    df["sim_true_date"] = df.true_date.dt.strftime("%m%d")
    df["sim_crawl_date"] = df.crawl_date.dt.strftime("%m%d")

    return df





def output_excel(df_lst, out_file_name="out", out_file_path=None, sheet_name_lst=None):
    from pandas import ExcelWriter
    if out_file_path is None:
        # 如果没有out_file_path: 默认放在桌面
        out_file_path = f"{FILE_PATH_FOR_DESKTOP}/{out_file_name}.xlsx"
    with ExcelWriter(out_file_path) as writer:
        for i, df in enumerate(df_lst):
            if sheet_name_lst:
                sheet_name = sheet_name_lst[i]
            else:
                sheet_name = f"sheet_{i}"
            df.to_excel(writer, sheet_name, index=False)
        writer.save()















def avg(lst):
    if isinstance(lst, list):
        if len(lst) <1:
            # raise myError("元素小于1!")
            return 0
    elif isinstance(lst, type(pd.Series())):
        if lst.size <1:
            # raise myError("元素小于1!")
            return 0
    sum = 0
    for count, e in enumerate(lst):
        # print(count, e)
        sum += int(float(e))
    lst_avg = sum/(count+1)
    # print(lst_avg)
    return int(lst_avg)


def merge_df(
    x_name, y_name, out_file_name="out",
    is_df=None, join_field="house_id", output=True):
    """
    function: 不仅可以合并df/csv, 还附带输出csv的功能
    """
    print(">>>1")
    if not is_df:
        # 如果 不是df， 就把这个当做文件名，导入
        x_df = import_data(x_name, is_df=True)
        y_df = import_data(y_name, is_df=True)
    else:
        # 如果 是df， 就直接把传入的x、y当做 df对象来使用
        x_df = x_name
        y_df = y_name
    print(">>>2")
    # pd.merge() 返回的不是df类型，而是function类型。 但这个function可以使用to_csv导出文件
    #  ??????   什么情况？ 之前测试的时候返回的不是df对象，现在测试发现又确实是df对象了。。。见鬼！
    merged_df = pd.merge(x_df, y_df, how="left", on=join_field)
    if not output:
        return merged_df
    print(">>>3")
    merged_df.to_csv(FILE_PATH_FOR_DESKTOP+"/{0}.csv".format(out_file_name), index=False, encoding="gb18030")
    print("合并成功!")

# merge_df("aaa", "bbb", out_file_name="zzzz")
# exit()


# def k_top(lst, top=1):
#     if isinstance(lst, list):
#         if len(lst) <1:
#             # raise myError("元素小于1!")
#             return 0
#     elif isinstance(lst, type(pd.Series())):
#         if lst.size <1:
#             # raise myError("元素小于1!")
#             return 0
#
#     lst = sorted(lst)
#     return lst[top-1]


class NumpyEncoder(json.JSONEncoder):
    """ Special json encoder for np types """
    def default(self, obj):
        if isinstance(obj, (np.int_, np.intc, np.intp, np.int8,
                            np.int16, np.int32, np.int64, np.uint8,
                            np.uint16, np.uint32, np.uint64)):
            return int(obj)
        elif isinstance(obj, (np.float_, np.float16, np.float32,
                              np.float64)):
            return float(obj)
        elif isinstance(obj, (np.ndarray,)):
            return obj.tolist()
        return json.JSONEncoder.default(self, obj)










def k_divide(lst, piece=5):
    """
    function: 按lst从小到大的顺序, 等分成piece份 小lst 返回
    """
    if isinstance(lst, list):
        if len(lst) <1:
            # raise myError("元素小于1!")
            return 0
    elif isinstance(lst, type(pd.Series())):
        if lst.size <1:
            # raise myError("元素小于1!")
            return 0

    lst = sorted(lst)
    # 1. 打印原lst
    print(lst)
    node_order_lst = []
    node_lst = []
    for count in range(1, piece):
        node_order_value = round(len(lst) * (1/piece) * count) - 1 # 减一别忘了 (另外,这里返回的是顺序值,不是真实值)
        node_order_lst.append(node_order_value)
        node_lst.append(lst[node_order_value])
    # 2. 打印分好piece后的, 节点的顺序
    print(node_order_lst) # 是顺序
    print("值的lst: {}".format(node_lst)) # 是值

    piece_dict = {}
    count = 0
    while True:
        if count == piece:
            break
        elif count == 0:
            piece_dict.update({count+1 : lst[ : node_order_lst[count]+1]})
        elif count == piece-1:
            piece_dict.update({count+1 : lst[node_order_lst[count-1]+1 : ]})
        else:
            piece_dict.update({count+1 : lst[node_order_lst[count-1]+1 : node_order_lst[count]+1]})
        count += 1
    # 3. 打印根据上面的顺序, piece等拆分了lst后的dict
    print(piece_dict)
    return node_lst
    # return piece_dict


    # piece_lst = [] count = 0
    # while True:
    #     if count == piece:
    #         break
    #     elif count == 0:
    #         piece_lst.append(lst[ : node_order_lst[count]+1])
    #     elif count == piece-1:
    #         piece_lst.append(lst[node_order_lst[count-1]+1 : ])
    #     else:
    #         piece_lst.append(lst[node_order_lst[count-1]+1 : node_order_lst[count]+1])
    #     count += 1
    # # 3. 打印根据上面的顺序, piece等拆分了lst后的lst
    # print(piece_lst)
    # return piece_lst

# k_divide([3, 4, 5, 7, 2, 4, 46, 6, 7, 84, 4,5], 5)




def is_notnan_numeric(x):
    """
        numeric: 指所有数值: int/float (包括np.nan) (不包括None) (不包括'可以转成float的str')
        notnan_numeric: 指所有'非nan'的数值: int/float (不包括np.nan, 不包括None)
    """
    # 1. 若是数据集, 则直接返回False
    if isinstance(x, list) or isinstance(x, dict) or isinstance(x, set) or isinstance(x, tuple) or isinstance(x, np.ndarray):
        return False
    # 2. 是否为 None
    if x is None:
        return False
    # 3. 是否为 np.nan
    elif pd.isnull(x):
        return False
    # 4. 是否为 str
    elif isinstance(x, str):
        ### 注意: 这里防止x为可以被转成float的str, 先对str类型单独处理 (避免下一步造成错误判断)
        return False
    else:
        try:
            # 4. 如果可以被float()转化成float, 则x是为数值型, 返回True
            return isinstance(float(x), float)
        except:
            # 5. 不能转化, 则说明不是数值型
            return False


def safely_to_int(x, need_to_print=False):
    """
        save: 表示可以'安全'转化成'int'. 如果x为不能转化成int的数据, 则保留原样
        notice: 该函数是以'四舍五入'的方式转成int
    """
    # 如果是'非nan数值型', 则直接round()
    if is_notnan_numeric(x):
        ### 为了保证转成int, 需要先四舍五入, 再转成int
        ### 注意: 如果x=np.float(3.5000) , round(x, 0)  >>> 4.0 (还是会带个小数点,很烦,所以干脆转成int是最省心/最干净的)
        return int(round(x, 0))
    # 否则: 原样return回去
    else:
        if need_to_print:
            print(f"x: {x}, 类型为: {type(x)}, 不能保留整数!\n")
        return x


def round_df(df, round_digit=0, inplace=False):
    """
        默认:
            1. 四舍五入到整数
            2. 列名为"xx率"的, 一律以附带"百分号", 以str的形式呈现
    """
    if inplace is False:
        df = copy.deepcopy(df)

    for column, dtype in df.dtypes.items():
        # 1. 有些'率'是需要转化成'百分数'的
        if "率" in column:
            df[column] = df[column].apply(lambda x: format(x, ".2%"))
        # 2. 若发现df中的某列是 int型或者float型, 则按照round_digit四舍五入
        else:
            if dtype == np.dtype(np.float64) or dtype == np.dtype(np.int64):
                df[column] = df[column].round(round_digit)
    return df
















if __name__ == '__main__':
    print("start!")
    df = import_data("业务反馈调价", is_df=True)
    print(df)
    print(df.shape)
    print("end!")
