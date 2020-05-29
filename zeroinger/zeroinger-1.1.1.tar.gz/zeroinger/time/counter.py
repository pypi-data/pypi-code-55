import time
from zeroinger.time.stopwatch import StopWatch
from logzero import logger


class Counter:
    def __init__(self, name, log_interval=100, total_count=None):
        """
        计数器
        :param name: 提示关键字
        :param log_interval: 日志打印间隔
        :param total_count: 预期计数总量，用于计算进度百分比，可空
        """
        self.name = name
        self.timer = StopWatch.create_instance()
        self.count_value = 0
        self.log_interval = log_interval
        self.total_count = total_count

    def count(self, value=1):
        """
        进行累加
        :param value: 累加值，默认为1
        :return:
        """
        self.count_value += value
        if self.count_value % self.log_interval == 0:
            if self.total_count is None:
                logger.info('{}|{}ms|{}'.format(self.name, self.timer.duration(), self.count_value))
            else:
                logger.info(
                    '{}|{}ms|{}/{}={}'.format(self.name, self.timer.duration(), self.count_value, self.total_count,
                                              self.count_value / max(self.total_count, 1)))

    def get_value(self) -> int:
        """
        获取当前计数的值
        :return:
        """
        return self.count_value

    def reset(self):
        """
        重置，时间和计数清0
        :return:
        """
        self.timer = StopWatch.create_instance()
        self.count_value = 0
        pass
