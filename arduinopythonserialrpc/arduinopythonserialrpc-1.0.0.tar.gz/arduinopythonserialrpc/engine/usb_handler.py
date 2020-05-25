from threading import Event
from time import sleep

import serial
from serial import STOPBITS_ONE, PARITY_NONE, EIGHTBITS

from arduinopythonserialrpc.engine.protocol_to_arduino import ProtocolToArduino


class UsbHandler:
    def __init__(self, port_name: str, baud_rate: int, ctrl):
        self.port_name = port_name
        self.baud_rate = baud_rate
        self.serial = None
        self.usb_agent = None
        self.controller = ctrl
        self.calling_on_air = Event()
        self.result_incoming = Event()
        self.result_of_call_value = None

    def initialize(self) -> serial.Serial:
        self.serial = serial.Serial(port=self.port_name,
                                    baudrate=self.baud_rate,
                                    bytesize=EIGHTBITS,
                                    parity=PARITY_NONE,
                                    stopbits=STOPBITS_ONE)
        sleep(2)  # Wait the card to be ready
        return self.serial

    def disconnect(self):
        self.serial.close()

    def port_scanner(self):
        pass

    def get_card_name(self):
        return self.execute_remote_function_str("GetCardName", "")

    def close(self):
        self.serial.close()

    def execute_remote_function(self, function_name: str):
        self.calling_on_air.clear()
        ProtocolToArduino.send_command(function_name, self.serial)
        self.calling_on_air.set()
        self.result_incoming.wait()  # Note: This wait must be executed in order to preserve the Events handshaking

    def execute_remote_function_str(self, function_name: str, arg: str) -> str:
        self.calling_on_air.clear()
        ProtocolToArduino.send_command_str(function_name, arg, self.serial)
        self.calling_on_air.set()
        self.result_incoming.wait()
        return str(self.result_of_call_value)

    def execute_remote_function_int_int(self, function_name: str, arg1: int, arg2: int) -> int:
        self.calling_on_air.clear()
        ProtocolToArduino.send_command_int_int(function_name, arg1, arg2, self.serial)
        self.calling_on_air.set()
        self.result_incoming.wait()
        return int(self.result_of_call_value)

    def execute_remote_function_float(self, function_name: str, arg: float) -> float:
        self.calling_on_air.clear()
        ProtocolToArduino.send_command_float(function_name, arg, self.serial)
        self.calling_on_air.set()
        self.result_incoming.wait()
        return float(self.result_of_call_value)

    def get_port_name(self) -> str:
        return self.port_name

    def get_baud_rate(self) -> int:
        return self.baud_rate

    def set_incoming_result(self, value: str):
        self.result_incoming.set()
        self.calling_on_air.wait()
        self.result_of_call_value = value
        self.result_incoming.clear()
