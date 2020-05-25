from threading import Thread

from arduinopythonserialrpc.engine.protocol_from_arduino import ProtocolFromArduino
from arduinopythonserialrpc.exception.remote_exception import RemoteException


class UsbReceiverAgent(Thread):
    def __init__(self, input_stream, ctrl, usb_handler):
        super(UsbReceiverAgent, self).__init__(target=self.serial_listener, args=(1,))
        self.input = input_stream
        self.controller = ctrl
        self.usb_handler = usb_handler
        self.is_in_life = True
        self.calling_result = None

    def disconnect(self):
        self.is_in_life = False

    def serial_listener(self, fake):
        self.input.reset_input_buffer()
        while self.is_in_life:
            try:
                preamble = ProtocolFromArduino.get_token(self.input)
                if len(preamble) > 0:
                    self.calling_result = ProtocolFromArduino.handle_receiving_data(preamble, self.input, self.controller)
                    self.usb_handler.set_incoming_result(self.calling_result)
            except RemoteException as ex:
                print("Arduino raises an exception: " + str(ex))
            except Exception as ex:
                print("Local exception: " + str(ex))
