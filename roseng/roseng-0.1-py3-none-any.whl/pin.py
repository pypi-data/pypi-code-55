from abc import ABC, abstractmethod


class IOFlow():
    DEFAULT = 0
    IN = 1
    OUT = 2
    INOUT = 3


class IOType():
    GENERAL = 0
    PWM = 1
    ANA = 2
    SDA = 3
    SCL = 4
    MISO = 5
    MOSI = 6
    SCLK = 7


class Pin(ABC):

    def __init__(self, num: int, flow: IOFlow = IOFlow.OUT, type: IOType = IOType.GENERAL, tag: str = ''):
        super().__init__()
        self.num = num
        self.flow = flow
        self.type = type
        self.tag = tag

    def on_setup(self, host: 'Board'):
        pass

    def __eq__(self, other):
        return type(self) == type(other) and self.num == other.num and self.type == other.type

    def __str__(self):
        return 'Num:%s Flow:%s Type:%s' % (self.num, self.flow, self.type)


class DIGPin(Pin):

    @abstractmethod
    def input(self) -> int:
        pass

    @abstractmethod
    def output(self, val: int):
        pass


class ANAPin(Pin):

    @abstractmethod
    def input(self) -> float:
        pass

    @abstractmethod
    def output(self, val: float):
        pass


class PWMPin(Pin):

    def __init__(self, num: int, tag: str = ''):
        super().__init__(num, IOFlow.OUT, IOType.PWM, tag)

    @abstractmethod
    def start(self, dc: int = 0):
        pass

    @abstractmethod
    def stop(self):
        pass

    @abstractmethod
    def change_frequency(self, freq: int):
        pass

    @abstractmethod
    def change_duty_cycle(self, dc: int):
        pass


class SDAPin(Pin):

    def __init__(self, num: int, tag: str = ''):
        super().__init__(num, IOFlow.INOUT, IOType.SDA, tag)


class SCLPin(Pin):

    def __init__(self, num: int, tag: str = ''):
        super().__init__(num, IOFlow.DEFAULT, IOType.SCL, tag)


class MISOPin(Pin):

    def __init__(self, num: int, tag: str = ''):
        super().__init__(num, IOFlow.OUT, IOType.MISO, tag)


class MOSIPin(Pin):

    def __init__(self, num: int, tag: str = ''):
        super().__init__(num, IOFlow.IN, IOType.MOSI, tag)


class SCLKPin(Pin):

    def __init__(self, num: int, tag: str = ''):
        super().__init__(num, IOFlow.DEFAULT, IOType.SCLK, tag)
