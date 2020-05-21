# 进度类
class progress():
    def __init__(self, maxlen: int, progressname=""):
        self.__index = 0
        self.__maxlen = maxlen
        self.__progressname = progressname

    # 进度显示
    def printProgress(self):
        p_str = str(self.__index) + "/" + str(self.__maxlen)
        if self.__index < self.__maxlen:
            print('\r' + p_str, end="")
        else:
            print('\r' + p_str)
            print(self.__progressname + "已完成...")

    # 百分比进度显示
    def printProgressDegree(self):
        p = 100 * self.getDegree()
        if self.__index < self.__maxlen:
            print('\r%.2f%%' % p, end="")
        else:
            print('\r%.2f%%' % p)
            print(self.__progressname + "已完成...")

    # 进度条输出
    def printProgressBar(self):
        p = 100 * self.getDegree()
        pi = int(p / 5)
        temp = list()
        for i in range(20):
            if i < pi:
                temp.append("▉")
            else:
                temp.append("  ")
        if self.__index < self.__maxlen:
            print('\r' + "".join(temp) + '|%.2f%%' % p, end="")
        else:
            print('\r' + "".join(temp) + '|%.2f%%' % p)  # ▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉
            print(self.__progressname + "已完成...")

    # 获取最大值
    def getMaxlen(self):
        return self.__maxlen

    # 获取当前进展值
    def getIndex(self):
        return self.__index

    # 获取百分比进程
    def getDegree(self) -> float:
        return self.__index / self.__maxlen

    # 进度增加
    def add(self, i: int = 1):
        self.__index = (self.__index + i) if self.__index + i <= self.__maxlen else self.__maxlen

    # 重置进度类状态
    def reset(self, maxlen=-1):
        self.__index = 0
        if maxlen > 0:
            self.__maxlen = maxlen

    # 监听进度
    def thread_Listening(self, data):
        import threading
        import time
        def temp(data):
            while len(data) < self.__maxlen:
                time.sleep(1)
                self.__index = len(data)
                self.printProgressBar()

        threading.Thread(target=temp, args=(data,)).start()
        print('开始监听进度...')
