# #针对大目录下保留部分子目录的程序化处理方案
# 1.从大目录列出下一级目录,匹配是否是需要保留的子目录的前缀,如果不是,保存到待删除dir_list
# 2.如果是父目录，则判断是否等于待排除目录，如果等于，则不做处理，不等于则继续下沉
# 3.递归获取下一级目录,先判断获取的目录list是否为空，如果为空，则不做处理，否则将list中的key存入队列
# 4.处理到队列为空
import os
from queue import Queue

q = Queue()


def get_complex_list(key, exclude_list):
    target_list = []
    # 队列初始化
    q.put(key)
    while not q.empty():
        # 判断当前目录是否是将要排除的目录的父目录
        get_key = q.get()
        is_parent = is_parent_path_for_list(get_key, exclude_list)
        # 如果不是放入目标list, 是则获取下层目录放入队列
        if not is_parent:
            target_list.append(get_key)
        # 如果是进行二次判断，是否等于将要排除的目录
        else:
            # 如果目录不等于将要排除的目录，则进行下沉
            if not is_equal_for_list(get_key, exclude_list):
                tmp_list = get_sub_list(get_key)
                # 如果tmp_list不为空则存入队列进行下一轮循环
                if tmp_list:
                    for tmp in tmp_list:
                        q.put(tmp)
    return target_list


def is_parent_path_for_list(parent_path, path_list):
    is_parent_list = [is_parent_path(parent_path, path) for path in path_list]
    return any(is_parent_list)


def is_equal_for_list(parent_path, path_list):
    is_equal_list = [parent_path == path for path in path_list]
    return any(is_equal_list)


def is_parent_path(parent_path, path):
    return path.startswith(parent_path)


def get_sub_list(key):
    key = key if key.endswith('/') else key + '/'
    s3_ls_cmd = "aws s3 ls {key}".format(key=key)
    p = os.popen(s3_ls_cmd)
    ret = p.read()
    p.close()
    catalog_list = [item.lstrip() for item in ret.split('\n')]
    s3_key_list = ["{key}{new_key}".format(key=key, new_key=catalog[4:]) for catalog in catalog_list if
                   catalog != '' and catalog.endswith('/')]
    print(s3_key_list)
    return s3_key_list


if __name__ == '__main__':
    parent_path = 's3://cf-data-sync/export/finance/'
    path_list = ['s3://cf-data-sync/export/finance/goods_return_barcode_detail/2020-03-31/']
    result = get_complex_list(parent_path, path_list)
    print(result)
