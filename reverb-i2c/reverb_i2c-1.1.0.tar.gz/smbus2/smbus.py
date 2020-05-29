import os
import json

I2C_SMBUS_BLOCK_MAX = 32

PROJECT_ROOT = os.path.abspath(os.getcwd())
if "pfs" not in PROJECT_ROOT:
    raise RuntimeError("This package must be run within the TJREVERB pFS directory!")
while not PROJECT_ROOT.endswith("pfs"):
    PROJECT_ROOT = os.path.dirname(PROJECT_ROOT)
PROJECT_ROOT = os.path.dirname(PROJECT_ROOT, "pfs-output")


class SMBus:

    def __init__(self, bus):
        self.open(bus)

    def open(self, bus):
        self.path = os.path.join(PROJECT_ROOT, f"i2c-{bus}")

    def close(self):
        if self.fd:
            self.fd.close()
            self.fd = None

    def _read_address(self, addr):
        with open(os.path.join(self.path, f"{addr}.state"), 'r') as r:
            return json.load(r)

    def _write_address(self, addr, registers):
        with open(os.path.join(self.path, f"{addr}.command"), "w") as w:
            json.dump(registers, w)

    def read_i2c_block_data(self, address, value, length):
        if length > I2C_SMBUS_BLOCK_MAX:
            raise ValueError("Desired block length over %d bytes" % I2C_SMBUS_BLOCK_MAX)

        register = self._read_address(address)

        if value not in register:
            return [0 for _ in range(length)]
        if length > len(register[value]):
            return [*register[value], *[0 for _ in range(length-len(register[value]))]]
        else:
            return register[value]

    def write_i2c_block_data(self, address, value, commands):

        if len(commands) < I2C_SMBUS_BLOCK_MAX:
            raise ValueError("Desired block length over %d bytes" % I2C_SMBUS_BLOCK_MAX)

        register = self._read_address(address)
        register[value] = commands

        self._write_address(address, register)




