from typing import Optional, List
import logging
from pyvisa import ResourceManager
from pyvisa.resources import SerialInstrument

logger = logging.getLogger(__name__)


class KeithleyPS:
    def __init__(self, serial_port: Optional[str]=None, baud_rate: int=38400, instrument_name: Optional[str]=None, instrument_index: int=0, channels: int=3):
        self.logger = logger.getChild(self.__class__.__name__)

        resources = ResourceManager()

        if serial_port is not None:
            self.instrument: SerialInstrument = resources.open_resource(serial_port)
        else:
            instruments = resources.list_resources()

            if instrument_name is not None:
                if instrument_name not in instruments:
                    raise KeithleyPSNotFound(f'Power supply with name "{instrument_name}" not found')
            else:
                if instrument_index >= len(instruments):
                    raise KeithleyPSNotFound(f'Power supply with index "{instrument_index}" not found in list: {instruments}')

                instrument_name = instruments[instrument_index]

            self.instrument: SerialInstrument = resources.open_resource(instrument_name, baud_rate=baud_rate)

        self.instrument.read_termination = '\n'
        self.instrument.write_termination = '\n'
        self.instrument.send_end = True
        self.logger.info(f'Connected to "{instrument_name}" ({self.info})')
        self.channels = [KeithleyPSChannel(self, channel) for channel in range(0, channels)]

    @property
    def info(self) -> str:
        return self.instrument.query('*IDN?')


class KeithleyPSChannel:
    def __init__(self, ps: KeithleyPS, channel: int):
        self.ps = ps
        self.channel = channel

    def set_channel(self):
        self.ps.instrument.write(f'INST:NSEL {self.channel + 1}')

    def query(self, command: str) -> str:
        self.set_channel()
        return self.ps.instrument.query(command)

    def write(self, command: str):
        self.set_channel()
        self.ps.instrument.write(command)

    @property
    def voltage(self) -> float:
        return float(self.query('MEAS:VOLT:DC?'))

    @voltage.setter
    def voltage(self, value: float):
        self.write(f'VOLT {value}')

    @property
    def current(self) -> float:
        return float(self.query('MEAS:CURR:DC?'))

    @current.setter
    def current(self, value: float):
        self.write(f'CURR {value}')

    @property
    def output(self) -> bool:
        return self.query('CHAN:OUTP?') == '1'

    @output.setter
    def output(self, value: bool):
        self.write('CHAN:OUTP {1 if value else 0}')

    def on(self):
        self.write('CHAN:OUTP 1')

    def off(self):
        self.write('CHAN:OUTP 0')

    def set(self, voltage: Optional[float]=None, current: Optional[float]=None, on: Optional[bool]=None):
        if voltage is not None:
            self.voltage = voltage

        if current is not None:
            self.current = current

        if on is not None:
            self.output = on


class KeithleyPSError(Exception):
    pass


class KeithleyPSNotFound(KeithleyPSError):
    pass


if __name__ == '__main__':
    ps = KeithleyPS('ASRLCOM4')
    print(ps)
