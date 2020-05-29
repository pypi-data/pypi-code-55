from unittest import TestCase
from zeroinger.time.counter import Counter

class TestCounter(TestCase):
    def test(self):
        counter = Counter('测试counter')
        for i in range(203):
            counter.count()
    def test2(self):
        counter = Counter('测试counter',log_interval=10,total_count=400)
        for i in range(203):
            counter.count()

