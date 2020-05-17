import asyncio
import smbus  # type: ignore
from typing import Dict, Any

from yaqd_core import Sensor

from .__version__ import __branch__


channel_mapping = {}
channel_mapping["channel01"] = 0b000
channel_mapping["channel03"] = 0b001
channel_mapping["channel13"] = 0b010
channel_mapping["channel23"] = 0b011
channel_mapping["channel0"] = 0b100
channel_mapping["channel1"] = 0b101
channel_mapping["channel2"] = 0b110
channel_mapping["channel3"] = 0b111

fsr_mapping = {}
fsr_mapping[6.144] = 0b000
fsr_mapping[4.096] = 0b001
fsr_mapping[2.048] = 0b010
fsr_mapping[1.024] = 0b011
fsr_mapping[0.512] = 0b100
fsr_mapping[0.256] = 0b101

rate_mapping = {}
rate_mapping[8] = 0b000
rate_mapping[16] = 0b001
rate_mapping[32] = 0b010
rate_mapping[64] = 0b011
rate_mapping[128] = 0b100
rate_mapping[250] = 0b101
rate_mapping[475] = 0b110
rate_mapping[860] = 0b111


class ADS1115(Sensor):
    _kind = "ads1115"
    _version = "1.0.0" + f"+{__branch__}" if __branch__ else ""
    traits = ["uses-i2c", "uses-serial"]
    defaults: Dict[str, Any] = {}

    def __init__(self, name, config, config_filepath):
        super().__init__(name, config, config_filepath)
        self.fsr = config["fsr"]
        self.rate = config["rate"]
        self.address = config["i2c_addr"]
        self.bus = smbus.SMBus(1)
        # populate channels metadata
        self.channel_names = []
        self.channel_units = {}
        for c in config["channels"]:
            self.channel_names.append(f"channel{c}")
            self.channel_units[f"channel{c}"] = "V"

    async def _measure(self):
        out = {}
        for key in self.channel_names:
            # write to the config register
            config_byte_0 = 0x00
            config_byte_0 |= 1 << 7  # start a single conversion
            config_byte_0 |= channel_mapping[key] << 4
            config_byte_0 |= fsr_mapping[self.fsr] << 1
            config_byte_0 |= 1  # single-shot mode
            config_byte_1 = 0x00
            config_byte_1 |= rate_mapping[self.rate] << 5
            config_byte_1 |= 0 << 4  # traditional comparitor
            config_byte_1 |= 0 << 3  # comparitor active low
            config_byte_1 |= 0 << 2  # non-latching comparitor
            config_byte_1 |= 0b11  # disable comparitor
            self.bus.write_i2c_block_data(self.address, 0x01, [config_byte_0, config_byte_1])
            # wait for conversion to complete
            while True:
                config = self.bus.read_i2c_block_data(self.address, 0x01, 2)
                if config[0] >= 128:
                    break
                await asyncio.sleep(0.1)
            # write to address pointer
            #  this appears in the datasheet
            #  but I don't completely understand it
            #  perhaps it clears the conversion register?
            #  - Blaise 2020-03-09
            self.bus.write_byte(self.address, 0x00)
            # read from conversion register
            data = self.bus.read_i2c_block_data(self.address, 0x00, 2)
            v = data[0] << 8 | data[1]
            if v > 128:
                v = -(2 ** 16) + v
            v *= self.fsr
            v /= 2 ** 16
            v *= 2
            out[key] = v
            await asyncio.sleep(0.1)
        return out
