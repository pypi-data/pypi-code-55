from producer.producer1 import producer1
from common.utils.Configuration import Configuration
class producer2:
    def __init__(self):
        p1 = producer1()
        c = Configuration()
        print("Producer2")