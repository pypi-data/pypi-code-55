# 定义dict_keys_list
def dict_keys_list(dict):
    res =  [i for i in dict.keys()]
    return res
# 定义dict_values_list
def dict_values_list(dict):
    res = [i for i in dict.values()]
    return res
def paste(list:dict(type=list,help="一维数组"),sep:dict(type=str,help="seperater default value is |")="|")->str:
	return sep.join(list)
# 元组转化为列表
def tuple_as_list(tuple):
	return(list(tuple))
# 取两个列表的交集
def list_intersect(list1,list2):
	return list(set(list1).intersection(set(list2)))
# 取两个列表的并集
def list_union(list1,list2):
	return list(set(list1).union(set(list2)))
# 取第2个列表有第一个没有的数据
def list_diff(list1,list2):
	return list(set(list2).difference(set(list1)))


if __name__ == "__main__":
	mydata = [1,2,3,4,5]
	myarr = [['A1'],['B1']]
	text = "|".join(['a',"b","c"])
	text2 = paste(['a','b','c'],"|")
	print(text2)
	print(type(text))
	print(paste.__annotations__)
	a = ["我是胡立磊"]
	b = "我是e"
	mydata2 =[['1','tom'],['2','jack']]
	tupledata = (1,2,3)
	listdata = tuple_as_list(tupledata)
	print(listdata)
	list1 = [1,2,3]
	list2 = [1,2,4]
	print(list_union(list1,list2))
	print(list_intersect(list1,list2))
	print(list_diff(list1,list2))
	list3=[[1,2],[3,4]]
	list4=[[1,2],[3,4],[5,6]]
	print(list_union(list3,list4))
	print(list_intersect(list3,list4))
	print(list_diff(list3,list4))
