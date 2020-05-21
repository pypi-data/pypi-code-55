import os
from os.path import join, getsize


def getdirsize(dir):
    size = 0
    for root, dirs, files in os.walk(dir):
        size += sum([getsize(join(root, name)) for name in files])
    size = ("%.2f" % (size / 1024 / 1024))
    print(size, "Mb")


def getwenjainjia(path):
    childs = []
    for root, dirs, files in os.walk(path):
        if root == path:
            childs.extend(dirs)
    for jia in childs:
        print(path + "\\" + jia)
        getdirsize(path + "\\" + jia)


# getwenjainjia(r"C:\Users\氵梦灵\Desktop\ooo")
