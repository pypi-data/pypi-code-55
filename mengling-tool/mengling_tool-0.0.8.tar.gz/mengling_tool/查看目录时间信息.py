import time
import os


# 把时间戳转化为时间: 1479264792 to 2016-11-16 10:53:12
def TimeStampToTime(timestamp):
    if type(timestamp) != float: return timestamp
    timeStruct = time.localtime(timestamp)
    return time.strftime('%Y-%m-%d %H:%M:%S', timeStruct)


def kuaipai(arr, lie):
    if len(arr) <= 1: return arr
    mid = arr[int(len(arr) / 2)][lie]
    zuo = [a for a in arr if a[lie] < mid]
    zho = [j for j in arr if j[lie] == mid]
    you = [y for y in arr if y[lie] > mid]
    return kuaipai(zuo, lie) + zho + kuaipai(you, lie)


def gettimes(path, lie):
    fs = []  # ("文件名", "创建时间", "修改时间", "访问时间")
    for root, dirs, files in os.walk(path):
        root1 = root.replace(path, "")
        for file in files:
            filename = root1 + "\\" + file
            ctime = os.path.getctime(path + filename)
            xtime = os.path.getmtime(path + filename)
            atime = os.path.getatime(path + filename)
            fs.append((filename, ctime, xtime, atime))
    fs = kuaipai(fs, lie)
    times = []
    for f in fs:
        temp = []
        for d in f:
            temp.append(TimeStampToTime(d))
        times.append(tuple(temp))
    times.insert(0, ("文件名", "创建时间", "修改时间", "访问时间"))
    for f in times:
        print(f[:])


# gettimes(r"C:\Users\氵梦灵\Documents\WeChat Files\ljh1321443305", 2)
