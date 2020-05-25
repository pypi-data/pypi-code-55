from arduinopythonserialrpc.engine.usb_handler import UsbHandler
from arduinopythonserialrpc.exception.local_exception import LocalException


class ActionSelector:
    @staticmethod
    def select_and_execute(usb_handler: UsbHandler, action_name: str, arg1=None, arg2=None):
        if action_name is not None and len(action_name) > 0:
            if arg2 is not None:
                if arg1 is not None:
                    return ActionSelector.exec_three(usb_handler, action_name, arg1, arg2)
                else:
                    raise LocalException("Error calling " + action_name +
                                         ": invalid empty first argument with the second argument: "+str(arg2))
            elif arg1 is not None:
                return ActionSelector.exec_two(usb_handler, action_name, arg1)
            else:
                return ActionSelector.exec_one(usb_handler, action_name)
        else:
            raise LocalException("Error: invalid empty action name")

    @staticmethod
    def exec_three(usb_handler: UsbHandler, action_name: str, arg1, arg2) -> int:
        if isinstance(arg1, int):
            if isinstance(arg2, int):
                return usb_handler.execute_remote_function_int_int(action_name, arg1, arg2)
            else:
                raise LocalException("Error calling " + action_name + ": invalid second argument type. Found " +
                                     type(arg2).__name__ + " instead of int")
        else:
            raise LocalException("Error calling "+action_name+": invalid first argument type. Found "
                                 +type(arg1).__name__+" instead of int")

    @staticmethod
    def exec_two(usb_handler: UsbHandler, action_name: str, arg1):
        if isinstance(arg1, str):
            return usb_handler.execute_remote_function_str(action_name, arg1)
        elif isinstance(arg1, float):
            return usb_handler.execute_remote_function_float(action_name, arg1)
        else:
            raise LocalException("Error calling "+action_name+": invalid argument type. Found "+type(arg1).__name__+" instead of str or float")

    @staticmethod
    def exec_one(usb_handler: UsbHandler, action_name: str):
        return usb_handler.execute_remote_function(action_name)
