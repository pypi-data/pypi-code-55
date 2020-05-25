from serial.rfc2217 import Serial

from arduinopythonserialrpc.engine.protocol_constants import VOID_ARG_PREAMBLE, STRING_ARG_PREAMBLE, INT_ARG_PREAMBLE, \
    INT_INT_ARG_PREAMBLE, FLOAT_ARG_PREAMBLE


class ProtocolToArduino:
    def __init__(self):
        pass

    @staticmethod
    def send_command(cmd: str, serial: Serial):
        body = cmd.strip() + " " + VOID_ARG_PREAMBLE
        serial.write(body.encode())
        serial.flush()

    @staticmethod
    def send_command_str(cmd: str, arg1: str, serial: Serial):
        body = cmd.strip() + " " + STRING_ARG_PREAMBLE + arg1
        serial.write(body.encode())
        serial.flush()

    @staticmethod
    def send_command_int(cmd: str, arg1: int, serial: Serial):
        body = cmd.strip() + " " + INT_ARG_PREAMBLE + str(arg1)
        serial.write(body.encode())
        serial.flush()

    @staticmethod
    def send_command_float(cmd: str, arg1: float, serial: Serial):
        body = cmd.strip() + " " + FLOAT_ARG_PREAMBLE + str(arg1)
        serial.write(body.encode())
        serial.flush()

    @staticmethod
    def send_command_int_int(cmd: str, arg1: int, arg2: int, serial: Serial):
        body = cmd.strip() + " " + INT_INT_ARG_PREAMBLE + str(arg1) + "," + str(arg2)
        serial.write(body.encode())
        serial.flush()
