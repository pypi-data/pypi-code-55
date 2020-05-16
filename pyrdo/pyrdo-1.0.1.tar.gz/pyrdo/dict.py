#定义两个列表转dict
def list_as_dict(list_keys,list_values):
    res = dict(zip(list_keys,list_values))
    return res
#检查文件中是否包含dict中的多个单词
def textSearch(key,dict):
    for x in range(len(dict)):
        item = key in dict[x]
        #print(item)
        if item :
            return True
            break
        else:
            continue
    return False
