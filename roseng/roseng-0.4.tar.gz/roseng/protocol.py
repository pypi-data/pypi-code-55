from abc import ABC, abstractmethod


class I2C(ABC):

    def __init__(self, addr: int, bus: int = 1):
        super().__init__()

    @abstractmethod
    def write_byte(self, reg: int, val: int):
        pass

    @abstractmethod
    def read_byte(self, reg: int) -> int:
        pass


class SPI(ABC):

    def __init__(self, bus: int = 0, client: int = 0):
        super().__init__()

    @abstractmethod
    def set_mode(self, mode: int):
        pass

    @abstractmethod
    def set_speed(self, hz: int):
        pass

    @abstractmethod
    def write_byte(self, val: int):
        pass

    @abstractmethod
    def read_byte(self, reg: int) -> int:
        pass


class Serial(ABC):

    def __init__(self, port: str, baudrates: int, timeout: float):
        super().__init__()

    @abstractmethod
    def read_bytes(self) -> bytes:
        pass

    @abstractmethod
    def write_bytes(self, data: bytes):
        pass
