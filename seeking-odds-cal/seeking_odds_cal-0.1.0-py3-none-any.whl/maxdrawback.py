import numpy as np

def maxdrawback(data):
    index_end = np.argmax(np.maximum.accumulate(data)-data) #end position
    print("max drawback date")
    print(index_end)
    index_beg = np.argmax(data[:index_end]) #begin position
    print('history high point date')
    print(index_beg)
    maxdrawvalue = data[index_end]-data[index_beg]
    maxdrawpercent = maxdrawvalue/data[index_beg]*100
    return maxdrawpercent

def maxdrawdown_list(data_list):
    """最大回撤率"""
    data_list = np.array(data_list)
    maxac = np.zeros(len(data_list))
    max_value = data_list[0]
    maxdrawdown_list = []
    for i in range(0, len(data_list)): #遍历数组，当其后一项大于前一项时
        if data_list[i] > max_value:
            max_value = data_list[i]
        maxac[i] = max_value
        if i == 0:
            maxdrawdown_list.append(0)
            continue

        end_idx = np.argmax((maxac[:i+1] - data_list[:i+1]) / maxac[:i+1])
        if end_idx == 0:
            maxdrawdown_list.append(0)
        else:
            start_idx = np.argmax(data_list[:end_idx])
            maxdrawdown_list.append((data_list[start_idx] - data_list[end_idx]) / data_list[start_idx])
    return maxdrawdown_list