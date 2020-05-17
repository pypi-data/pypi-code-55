# from . import list as rdlist
# write by Reshape Data
# 设置数组的长度

def arrayLen(arrayData):
    res = 0
    res = len(arrayData)
    return res


# 定义数据按列选择
def arrayColSel(arrayData, selector=[0, 1]):
    res = []
    for i in range(len(arrayData)):
        row = []
        for j in range(len(selector)):
            index = selector[j]
            row.append(arrayData[i][index])
        res.append(row)
    return res


# 使用表达式重新设计实现方式
def arrayColSel2(arrayData, ColIndex=0):
    # 使用列表表达式，代码更简洁
    res = [row[ColIndex] for row in arrayData]
    return res


# 定义数据按行进行选择
def arrayRowSel(arrayData, selector=[0, 1]):
    res = []
    for i in range(len(selector)):
        res.append(arrayData[selector[i]])
    return res


# 按数据列进行转换为小数
def arrayColNumeric(arrayData, colIndex, digit=2):
    res = []
    for i in range(len(arrayData)):
        row = []
        for j in range(len(arrayData[i])):
            if j == colIndex:
                row.append(round(float(arrayData[i][j]), digit))
            else:
                row.append(arrayData[i][j])
        res.append(row)
    return res


# 按数据列进行转换为整数
def arrayColInt(arrayData, colIndex, digit=2):
    res = []
    for i in range(len(arrayData)):
        row = []
        for j in range(len(arrayData[i])):
            if j == colIndex:
                row.append(int(arrayData[i][j]))
            else:
                row.append(arrayData[i][j])
        res.append(row)
    return res


# 向数据指定列复制值
def arrayInsertRepValue(arrayData, value, colIndex=0):
    res = []
    for i in range(len(arrayData)):
        row = arrayData[i]
        row.insert(colIndex, value)
        res.append(row)
    return res


# 向二维数据插入序号
def arrayInsertIndex(arrayData, index=-1):
    res = []
    if index == -1:
        idx = len(arrayData[0])
    else:
        idx = index
    for i in range(len(arrayData)):
        row = arrayData[i]
        row.insert(idx, i + 1)
        res.append(row)
    return res

#在数据指定列填写前缀
def arrayAddPrefix(arrayData,colIndex=0,prefix="问题",suffix=":",NumIndex=True):
	res = arrayData
	for i in range(len(arrayData)):
		if NumIndex :
			prefix_num = str(i + 1)
		else :
			prefix_num = ""
		res[i][colIndex] = prefix + prefix_num + suffix + arrayData[i][colIndex]
	return(res)

#设置数据的链接函数
def arrayPaste(arrayData, sep=",", collapse="\n"):
	res = []
	for i in range(len(arrayData)):
		res.append(sep.join(arrayData[i]))
	res2 = collapse.join(res)
	return (res2)

#定义数据查找函数
def arrayLookup(arrayData,txt_search,look_idx,ret_idx):
	for i in range(len(arrayData)):
		look_value = arrayData[i][look_idx]
		if txt_search == look_value:
			return arrayData[i][ret_idx]
			break
		else:
			continue
	return False
#定义子项为tuple转为列表
def array_tupleItem_as_list(tupleArray):
    res = []
    for i in range(len(tupleArray)):
        item = tupleArray[i]
        data = list(item)
        res.append(data)
    return res
#定义子项为list转为tuple
def array_listItem_as_tuple(listArray):
    res = []
    for i in range(len(listArray)):
        item = listArray[i]
        data = tuple(item)
        res.append(data)
    return res
def list_diff(list1,list2):
	return list(set(list2).difference(set(list1)))
# 针对两个二维护列表进行差集处理
def array_diff(array1,array2,id_index=1):
    index1 = arrayColSel2(array1,id_index)
    index2 = arrayColSel2(array2,id_index)
    sel_index = list_diff(index1,index2)
    res = []
    for i in range(len(array2)):
        item = array2[i]
        if item[id_index] in sel_index:
            res.append(item)
        else:
            pass
    return res




if __name__ == "__main__":
    mydata = [1,2,3,4,5]
    myarr = [['A1'],['B1']]
    myres = arrayAddPrefix(myarr,0)
    print(myres)
    text = "|".join(['a',"b","c"])
    print(text)
    myarr2 = arrayPaste(myarr)
    print(myarr2)
    a = ["我是胡立磊"]
    b = "我是e"
    mydata2 =[['1','tom'],['2','jack']]
    print(arrayLookup(mydata2,'jack',1,0))
    print(arrayColSel2(mydata2,0))
    mydata3 = [('caas', '0', 'root', '-1', 0), ('caas', '71688', '网商_test', '0', 0)]
    mydata4 = (array_tupleItem_as_list(mydata3))
    print(mydata4)
    mydata5 = array_listItem_as_tuple(mydata4)
    print(mydata5)
    myid = arrayColSel2(mydata5,1)
    print(myid)
    arr1 = [[1,'jack'],[2,'tom']]
    arr2 = [[1, 'jack'], [2, 'tom'],[3,'kalin']]
    diff = array_diff(arr1,arr2,0)
    print(diff)

