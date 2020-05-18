"""
This module implements an api for the op codes that can be sent to a device.

There are 16 sources available, of which 13 apply to the RCX:

Name                  Argument                  Description
Variable              Variable index, 0..31.    Returns value of specified
                                                variable.
Timer                 Timer index, 0..3.        Returns value of specified
                                                timer, in 1/100ths of a second.
Immediate             Immediate value.          Returns specified immediate
                                                value.
Motor State           Motor index, 0..2.        Returns state of specified
                                                motor. See below.
Random                Maximum value.            Returns random value, 0..max.
Reserved              N/A                       Cybermaster only.
Reserved              N/A                       Cybermaster only.
Reserved              N/A                       Cybermaster only.
Current Program       Ignored.                  Returns current program number.
Sensor Value          Sensor index, 0..2.       Returns value of specified
                                                sensor.
Sensor Type           Sensor index, 0..2.       Returns type of specified
                                                sensor.
Sensor Mode           Sensor index, 0..2.       Returns mode of specified
                                                sensor.
Raw Sensor Value      Sensor index, 0..2.       Returns raw value of specified
                                                sensor, 0..1023.
Boolean Sensor Value  Sensor index, 0..2.       Returns boolean value of
                                                specified sensor, 0..1.
Clock                 Must be 0.                Returns minutes since power on.
Message               Must be 0.                Returns value of message
                                                buffer.

"""

VARIABLE = 0
TIMER = 1
IMMEDIATE = 2
MOTOR_STATE = 3
RANDOM = 4
CURRENT_PROG = 8
SENSOR_VALUE = 9
SENSOR_TYPE = 10
SENSOR_MODE = 11
RAW_SENSOR_VALUE = 12
BOOL_SENSOR_VALUE = 13
CLOCK = 14
MESSAGE = 15

MOTOR_A = 0x01
MOTOR_B = 0x02
MOTOR_C = 0x04

MOTOR_OFF = 0x40
MOTOR_ON = 0x80
MOTOR_FLOAT = 0x00
MOTOR_ON_ = MOTOR_ON | MOTOR_OFF

MOTOR_DIR_FLIP = 0x40
MOTOR_DIR_FWD = 0x80
MOTOR_DIR_REV = 0x00
MOTOR_DIR_FLIP_ = MOTOR_DIR_FLIP | MOTOR_DIR_FWD

DISP_WATCH = 0
DISP_SENSOR_1 = 1
DISP_SENSOR_2 = 2
DISP_SENSOR_3 = 3
DISP_MOTOR_A = 4
DISP_MOTOR_B = 5
DISP_MOTOR_C = 6

SOUND_BLIP = 0
SOUND_BEEP_BEEP = 1
SOUND_DOWNWARD_TONES = 2
SOUND_UPWARD_TONES = 3
SOUND_LOW_BUZZ = 4
SOUND_FAST_UPWARD_TONES = 5

SENSOR_1 = 0
SENSOR_2 = 1
SENSOR_3 = 2
SENSOR_FIRST = SENSOR_1
SENSOR_LAST = SENSOR_3
SENSOR_RNG = (SENSOR_FIRST, SENSOR_LAST)

BYTE_BIT_SIZE = 8
BYTE_HEX_SIZE = 2
BYTE_RNG = (0, pow(2, BYTE_BIT_SIZE) - 1)
SHORT_BIT_SIZE = 16
SHORT_HEX_SIZE = 4
SHORT_RNG = (0, pow(2, SHORT_BIT_SIZE) - 1)
UNUSED_MAX = pow(2, SHORT_BIT_SIZE) - 1


sources = {
    VARIABLE: {
        "name": "Variable",
        "range": (0, 31),
        "description": "Returns value of specified variable.",
    },
    TIMER: {
        "name": "Timer",
        "range": (0, 3),
        "description": "Returns value of specified timer, in 1/100ths of a " "second.",
    },
    IMMEDIATE: {
        "name": "Immediate",
        "range": SHORT_RNG,
        "description": "Returns specified immediate value.",
    },
    MOTOR_STATE: {
        "name": "Motor State",
        "range": (0, 2),
        "description": "Returns state of specified motor. See below.",
    },
    RANDOM: {"name": "Random Maximum value.", "range": SHORT_RNG, "description": "-"},
    CURRENT_PROG: {
        "name": "Current Program",
        "range": (0, 0),
        "description": "Returns current program number.",
    },
    SENSOR_VALUE: {
        "name": "Sensor Value",
        "range": SENSOR_RNG,
        "description": "Returns value of specified sensor.",
    },
    SENSOR_TYPE: {
        "name": "Sensor Type",
        "range": SENSOR_RNG,
        "description": "Returns type of specified sensor.",
    },
    SENSOR_MODE: {
        "name": "Sensor Mode",
        "range": SENSOR_RNG,
        "description": "Returns mode of specified sensor.",
    },
    RAW_SENSOR_VALUE: {
        "name": "Raw Sensor Value",
        "range": SENSOR_RNG,
        "description": "Returns raw value of specified sensor, 0..1023",
    },
    BOOL_SENSOR_VALUE: {
        "name": "Boolean Sensor Value",
        "range": SENSOR_RNG,
        "description": "Returns boolean value of specified sensor, 0..1",
    },
    CLOCK: {
        "name": "Clock",
        "range": (0, 0),
        "description": "Returns minutes since power on.",
    },
    MESSAGE: {
        "name": "Message",
        "range": (0, 0),
        "description": "Returns value of message buffer.",
    },
}


op_codes = {
    "is_alive": {"description": "Alive, void", "arguments": None, "opcode": 0x10},
    "get_battery_power": {
        "description": "Get battery power, void",
        "arguments": None,
        "opcode": 0x30,
    },
    "get_memory_map": {
        "description": "Get memory map, void",
        "arguments": None,
        "opcode": 0x20,
    },
    "get_versions": {
        "description": "Get versions",
        "arguments": None,
        "opcode": 0x15,
        "default": [0x01, 0x03, 0x05, 0x07, 0x0B],
    },
    "power_off": {"description": "Power off, void", "arguments": None, "opcode": 0x60},
    "set_power_down_delay": {
        "description": "Set power down delay",
        "arguments": {"minutes": BYTE_RNG},
        "opcode": 0xB1,
    },
    "set_program_number": {
        "description": "Set program number",
        "arguments": {"program": (0, 4)},
        "opcode": 0x91,
    },
    "set_transmitter_range": {
        "description": "Set transmitter range",
        "arguments": {"range": (0, 1)},
        "opcode": 0xC6,
    },
    "send_message": {
        "description": "Tell RCX to send message, set_message is executed "
        "by RCX via its own IR",
        "arguments": {"source": [VARIABLE, IMMEDIATE], "argument": None},
        "source_type_range": {IMMEDIATE: BYTE_RNG},
        "opcode": 0xB2,
    },
    "set_message": {
        "description": "Set message in RCX mailbox",
        "arguments": {"message": BYTE_RNG},
        "opcode": 0xF7,
    },
    "set_display": {
        "description": "Set display",
        "arguments": {"source": [VARIABLE, IMMEDIATE], "argument": None},
        "source_type_range": {
            VARIABLE: [i for i in range(0, 31)].append(UNUSED_MAX),
            IMMEDIATE: [
                DISP_WATCH,
                DISP_SENSOR_1,
                DISP_SENSOR_2,
                DISP_SENSOR_3,
                DISP_MOTOR_A,
                DISP_MOTOR_B,
                DISP_MOTOR_C,
                UNUSED_MAX,
            ],
        },
        "opcode": 0x33,
    },
    "set_datalog_size": {
        "description": "allocate and initalize a datalog with space for the"
        "requested number of datalogs",
        "arguments": {"size": SHORT_RNG},
        "opcode": 0x52,
    },
    "datalog_next": {
        "description": "set next entry in datalog",
        "arguments": {
            "source": [VARIABLE, TIMER, SENSOR_VALUE, CLOCK],
            "argument": None,
        },
        "opcode": 0x62,
    },
    "get_datalog": {
        "description": "Upload datalog",
        "arguments": {"first_index": SHORT_RNG, "number_of_entries": SHORT_RNG},
        "opcode": 0xA4,
    },
    "get_value": {
        "description": "Get value, source, argument",
        "arguments": {
            "source": [
                VARIABLE,
                TIMER,
                MOTOR_STATE,
                CURRENT_PROG,
                SENSOR_VALUE,
                SENSOR_MODE,
                SENSOR_TYPE,
                RAW_SENSOR_VALUE,
                BOOL_SENSOR_VALUE,
                CLOCK,
                MESSAGE,
            ],
            "argument": None,
        },
        "opcode": 0x12,
    },
    "set_variable": {
        "description": "Set variable",
        "arguments": {
            "index": (0, 31),
            "source": [
                VARIABLE,
                TIMER,
                IMMEDIATE,
                MOTOR_STATE,
                RANDOM,
                CURRENT_PROG,
                SENSOR_VALUE,
                SENSOR_TYPE,
                SENSOR_MODE,
                RAW_SENSOR_VALUE,
                BOOL_SENSOR_VALUE,
                CLOCK,
                MESSAGE,
            ],
            "argument": None,
        },
        "opcode": 0x14,
    },
    "play_sound": {
        "description": "Play sound",
        "arguments": {
            "sound": [
                SOUND_BLIP,
                SOUND_BEEP_BEEP,
                SOUND_DOWNWARD_TONES,
                SOUND_UPWARD_TONES,
                SOUND_LOW_BUZZ,
                SOUND_FAST_UPWARD_TONES,
            ]
        },
        "opcode": 0x51,
    },
    "play_tone": {
        "description": """Play tone, frequency (short) (Hz),
                          duration (byte) (1/100th of a second)""",
        "arguments": {"frequency": SHORT_RNG, "duration": BYTE_RNG},
        "opcode": 0x23,
    },
    "set_motor_direction": {
        "description": "Set motor direction",
        "arguments": {
            "code": [
                MOTOR_A | MOTOR_DIR_REV,
                MOTOR_B | MOTOR_DIR_REV,
                MOTOR_C | MOTOR_DIR_REV,
                MOTOR_A | MOTOR_B | MOTOR_DIR_REV,
                MOTOR_A | MOTOR_C | MOTOR_DIR_REV,
                MOTOR_B | MOTOR_C | MOTOR_DIR_REV,
                MOTOR_A | MOTOR_B | MOTOR_C | MOTOR_DIR_REV,
                MOTOR_A | MOTOR_DIR_FWD,
                MOTOR_B | MOTOR_DIR_FWD,
                MOTOR_C | MOTOR_DIR_FWD,
                MOTOR_A | MOTOR_B | MOTOR_DIR_FWD,
                MOTOR_A | MOTOR_C | MOTOR_DIR_FWD,
                MOTOR_B | MOTOR_C | MOTOR_DIR_FWD,
                MOTOR_A | MOTOR_B | MOTOR_C | MOTOR_DIR_FWD,
                MOTOR_A | MOTOR_DIR_FLIP,
                MOTOR_B | MOTOR_DIR_FLIP,
                MOTOR_C | MOTOR_DIR_FLIP,
                MOTOR_A | MOTOR_B | MOTOR_DIR_FLIP,
                MOTOR_A | MOTOR_C | MOTOR_DIR_FLIP,
                MOTOR_B | MOTOR_C | MOTOR_DIR_FLIP,
                MOTOR_A | MOTOR_B | MOTOR_C | MOTOR_DIR_FLIP,
                MOTOR_A | MOTOR_DIR_FLIP_,
                MOTOR_B | MOTOR_DIR_FLIP_,
                MOTOR_C | MOTOR_DIR_FLIP_,
                MOTOR_A | MOTOR_B | MOTOR_DIR_FLIP_,
                MOTOR_A | MOTOR_C | MOTOR_DIR_FLIP_,
                MOTOR_B | MOTOR_C | MOTOR_DIR_FLIP_,
                MOTOR_A | MOTOR_B | MOTOR_C | MOTOR_DIR_FLIP_,
            ]
        },
        "opcode": 0xE1,
    },
    "set_motor_state": {
        "description": "Set motor on/off",
        "arguments": {
            "code": [
                MOTOR_A | MOTOR_FLOAT,
                MOTOR_B | MOTOR_FLOAT,
                MOTOR_C | MOTOR_FLOAT,
                MOTOR_A | MOTOR_B | MOTOR_FLOAT,
                MOTOR_A | MOTOR_C | MOTOR_FLOAT,
                MOTOR_B | MOTOR_C | MOTOR_FLOAT,
                MOTOR_A | MOTOR_B | MOTOR_C | MOTOR_FLOAT,
                MOTOR_A | MOTOR_ON,
                MOTOR_B | MOTOR_ON,
                MOTOR_C | MOTOR_ON,
                MOTOR_A | MOTOR_B | MOTOR_ON,
                MOTOR_A | MOTOR_C | MOTOR_ON,
                MOTOR_B | MOTOR_C | MOTOR_ON,
                MOTOR_A | MOTOR_B | MOTOR_C | MOTOR_ON,
                MOTOR_A | MOTOR_OFF,
                MOTOR_B | MOTOR_OFF,
                MOTOR_C | MOTOR_OFF,
                MOTOR_A | MOTOR_B | MOTOR_OFF,
                MOTOR_A | MOTOR_C | MOTOR_OFF,
                MOTOR_B | MOTOR_C | MOTOR_OFF,
                MOTOR_A | MOTOR_B | MOTOR_C | MOTOR_OFF,
                MOTOR_A | MOTOR_ON_,
                MOTOR_B | MOTOR_ON_,
                MOTOR_C | MOTOR_ON_,
                MOTOR_A | MOTOR_B | MOTOR_ON_,
                MOTOR_A | MOTOR_C | MOTOR_ON_,
                MOTOR_B | MOTOR_C | MOTOR_ON_,
                MOTOR_A | MOTOR_B | MOTOR_C | MOTOR_ON_,
            ]
        },
        "opcode": 0x21,
    },
    "set_motor_power": {
        "description": "Set motor power",
        "arguments": {
            "source": [VARIABLE, IMMEDIATE, RANDOM],
            "argument": None,
            "motors": [
                MOTOR_A,
                MOTOR_B,
                MOTOR_C,
                MOTOR_A | MOTOR_B,
                MOTOR_A | MOTOR_C,
                MOTOR_B | MOTOR_C,
                MOTOR_A | MOTOR_B | MOTOR_C,
            ],
        },
        "opcode": 0x13,
        "source_type_range": {IMMEDIATE: (0, 7)},
    },
    "wait": {
        "description": "Wait",
        "arguments": {"source": [VARIABLE, IMMEDIATE, RANDOM], "argument": None},
        "opcode": 0x43,
    },
    "set_time": {
        "description": "set current time",
        "arguments": {"hours": (0, 23), "minutes": (0, 59)},
        "opcode": 0x22,
    },
}


def _verify_range(rng, value, name):
    if isinstance(rng, list):
        if value not in rng:
            raise ValueError(
                f"argument '{name}' with value: {value}, " f"is not in range: {rng}"
            )
    if isinstance(rng, tuple):
        if not value >= rng[0] or not value <= rng[1]:
            raise ValueError(
                f"argument '{name}' with value: {value}, " f"is not in range: {rng}"
            )


def _correct_endian(hex_string):
    return f"{hex_string[2:4]}{hex_string[0:2]}"


def _get_hex_string(rng, value):
    if max(rng) <= 255:
        size = 2
        hex_string = f"{value:0{size}x}"
    if max(rng) > 255:
        size = 4
        hex_string_temp = f"{value:0{size}x}"
        hex_string = _correct_endian(hex_string_temp)
    return hex_string


def _set_defaults(op_code_name):
    arg_defaults = op_codes[op_code_name].get("default", None)
    defaults = []
    if arg_defaults:
        for value in arg_defaults:
            hex_string = _get_hex_string(BYTE_RNG, value)
            defaults.append(hex_string)
    return defaults


def _collect_other_args(args):
    return [
        (arg, rng) for arg, rng in args.items() if arg not in ["source", "argument"]
    ]


def _verify_and_build_cmd(op_code_name, **kwargs):
    _validate_input(op_code_name, **kwargs)
    return _build_raw_cmd(op_code_name, **kwargs)


def _build_raw_cmd(op_code_name, **kwargs):
    args = op_codes[op_code_name]["arguments"]
    opcode = op_codes[op_code_name]["opcode"]

    raw_cmd = [_get_hex_string(BYTE_RNG, opcode)]

    if not args:
        raw_cmd.extend(_set_defaults(op_code_name))
    else:
        other_args = _collect_other_args(args)
        if other_args:
            for (arg, rng) in other_args:
                hex_string = _get_hex_string(rng, kwargs[arg])
                raw_cmd.append(hex_string)

        if "source" in args:
            source = kwargs.get("source", None)
            arg = kwargs.get("argument", None)
            hex_string = _get_hex_string(BYTE_RNG, source)
            raw_cmd.append(hex_string)

            cfg_src_rng = op_codes[op_code_name].get("source_type_range", None)
            if cfg_src_rng and source in cfg_src_rng:
                hex_string = _get_hex_string(cfg_src_rng[source], arg)
                raw_cmd.append(hex_string)
            else:
                hex_string = _get_hex_string(sources[source]["range"], arg)
                raw_cmd.append(hex_string)

    return "".join(raw_cmd)


def _validate_input(op_code_name, **kwargs):

    args = op_codes[op_code_name]["arguments"]

    if args:
        too_many_args = [key for key in kwargs.keys() if key not in args.keys()]
        if too_many_args:
            raise ValueError(f"{too_many_args} not among valid arguments {args.keys()}")

        other_args = _collect_other_args(args)

        if other_args:
            for (arg, rng) in other_args:
                _verify_range(rng, kwargs[arg], arg)

        if "source" in args:
            source = kwargs.get("source", None)
            arg = kwargs.get("argument", None)

            if source not in args["source"]:
                raise ValueError(
                    f"source '{source}' not valid:\n"
                    f"should be one of:\n"
                    f"{sources}\n"
                    f"for function {op_code_name}"
                )

            if arg is None:
                raise ValueError(
                    f"missing required argument 'argument' "
                    f"expected for for source {sources[source]} "
                    f"for function {op_code_name}"
                )
            cfg_src_rng = op_codes[op_code_name].get("source_type_range", None)
            if cfg_src_rng and source in cfg_src_rng:
                _verify_range(cfg_src_rng[source], arg, "argument")
            else:
                _verify_range(sources[source]["range"], arg, "argument")


class RawFunctions:
    """This class provide an object api for op codes that can be sent the device.

    It requires an nqc object for access to the nqc binary and currently used serial
    interface.
    """

    def __init__(self, nqc_instance=None):
        """Init function, requires an nqc object instance."""
        if not nqc_instance:
            raise RuntimeError("No nqc instance provided.")

        self.nqc = nqc_instance

    def is_alive(self):
        """Check if device is alive."""
        cmd = _verify_and_build_cmd("is_alive")
        try:
            response = self.nqc.exec_raw(cmd)
        except IOError as e:
            response = 0
            if e.errno == 253:
                pass
            else:
                raise e
        return True if response == b"" else False

    def get_battery_power(self):
        """Return battery power in milivolts."""
        cmd = _verify_and_build_cmd("get_battery_power")
        response = self.nqc.exec_raw(cmd)
        norm_response = "".join(response.decode("utf-8").split())

        correct_norm_response = _correct_endian(norm_response)

        level = int(f"0x{correct_norm_response}", 16)
        return level

    def get_memory_map(self):
        """Return memory map on device."""
        raise NotImplementedError

    def set_transmitter_range(self, far=False):
        """Set transmitter range on device."""
        raise NotImplementedError

    def set_program_number(self, program):
        """Set program number for candidate program to run."""
        raise NotImplementedError

    def get_versions(self):
        """Return a dict with ROM and ROM version."""
        cmd = _verify_and_build_cmd("get_versions")
        response = self.nqc.exec_raw(cmd)
        norm_response = "".join(response.decode("utf-8").split())
        rom = (
            f"{_correct_endian(norm_response[0:4])}"
            f"{_correct_endian(norm_response[4:8])}"
        )
        firmware = (
            f"{_correct_endian(norm_response[8:12])}"
            f"{_correct_endian(norm_response[12:16])}"
        )
        return {
            "rom-firmware": rom,
            "ram-firmware": firmware,
            "desc-rom": (
                f"{int(norm_response[0:4],16)}." f"{int(norm_response[4:8],16)}"
            ),
            "desc-ram": (
                f"{int(norm_response[8:12],16)}." f"{int(norm_response[12:16],16)}"
            ),
        }

    def power_off(self):
        """Request device to power off."""
        cmd = _verify_and_build_cmd("power_off")
        response = self.nqc.exec_raw(cmd)
        return True if response == b"" else False

    def set_power_down_delay(self, minutes):
        """Set the amount of time in minutes to delay power off.

        A delay of 0 signifies that device should never power down.
        """
        cmd = _verify_and_build_cmd("set_power_down_delay", minutes=minutes)
        response = self.nqc.exec_raw(cmd)
        return True if response == b"" else False

    def send_message(self, source, argument):
        """Request device to send a message."""
        cmd = _verify_and_build_cmd("send_message", source=source, argument=argument)
        try:
            _ = self.nqc.exec_raw(cmd)
        except IOError as e:
            if e.errno == 253:
                pass
            else:
                raise e
        return True

    def set_message(self, message):
        """Set a message in the message box in a device."""
        cmd = _verify_and_build_cmd("set_message", message=message)
        try:
            _ = self.nqc.exec_raw(cmd)
        except IOError as e:
            if e.errno == 253:
                pass
            else:
                raise e
        return True

    def set_display(self, source, argument):
        """Request the display to show an device internal state.

        Such as sensor, motor etc.
        """
        cmd = _verify_and_build_cmd("set_display", source=source, argument=argument)
        response = self.nqc.exec_raw(cmd)
        return True if response == b"" else False

    def set_datalog_size(self, size):
        """Set datalog size."""
        cmd = _verify_and_build_cmd("set_datalog_size", size=size)
        response = self.nqc.exec_raw(cmd)
        return True if response == b"00 \n" else False

    def datalog_next(self, source, argument):
        """Set a value in the datalog and increment the datalog index by one."""
        cmd = _verify_and_build_cmd("datalog_next", source=source, argument=argument)
        response = self.nqc.exec_raw(cmd)
        return True if response == b"00 \n" else False

    def get_datalog(self, first_index, number_of_entries):
        """Upload the datalog to the host.

        The log is returned as a list of dicts containing datalog record
        source type, value, and source type index, e.g. which register
        value that was logged.
        """
        cmd = _verify_and_build_cmd(
            "get_datalog", first_index=first_index, number_of_entries=number_of_entries
        )
        response = self.nqc.exec_raw(cmd)
        norm_response = "".join(response.decode("utf-8").split())
        dlrec_size = BYTE_HEX_SIZE + SHORT_HEX_SIZE
        dlrec_list = []
        if norm_response != "00" and len(norm_response) / 6 == number_of_entries:
            for i in range(0, number_of_entries):
                index_type = i * dlrec_size
                index_value = (i * dlrec_size) + BYTE_HEX_SIZE

                types = {
                    (0xFF, 0xFF): (None, "Current datalog size"),
                    (0x00, 0x1F): (VARIABLE, "Variable"),
                    (0x20, 0x23): (TIMER, "Timer"),
                    (0x40, 0x42): (SENSOR_VALUE, "Sensor"),
                    (0x80, 0x80): (CLOCK, "Clock"),
                }
                dlrec_type = norm_response[index_type:index_value]
                dlrec_named_type = ""
                index_start = 0
                dlrec_source_type = None
                for key in types.keys():
                    type_value = int(f"0x{dlrec_type}", 16)
                    if type_value >= key[0] and type_value <= key[1]:
                        dlrec_named_type = types[key][1]
                        dlrec_source_type = types[key][0]
                        index_start = key[0]

                if not dlrec_named_type:
                    raise ValueError("{dlrec_type} is not among known types: {types}")
                dlrec_payload = _correct_endian(
                    norm_response[index_value: index_value + SHORT_HEX_SIZE]
                )
                if not dlrec_payload:
                    raise ValueError(
                        (
                            f"dlrec_type: {dlrec_type}, response: {response}, "
                            f"norm_response: {norm_response}, payload: {dlrec_payload}"
                        )
                    )
                dlrec = {
                    "source_type": dlrec_source_type,
                    "source_desc": dlrec_named_type,
                    "source_index": int(f"0x{dlrec_type}", 16) - index_start,
                    "value": int(f"0x{dlrec_payload}", 16),
                }
                dlrec_list.append(dlrec)

        return dlrec_list

    def get_value(self, source, argument):
        """Read a device internal state."""
        cmd = _verify_and_build_cmd("get_value", source=source, argument=argument)
        response = self.nqc.exec_raw(cmd)
        norm_response = _correct_endian("".join(response.decode("utf-8").split()))
        value = _get_hex_string(sources[source]["range"], int(f"0x{norm_response}", 16))

        return int(value, 16)

    def set_variable(self, index, source, argument):
        """Set a device register/variable to the requested value."""
        cmd = _verify_and_build_cmd(
            "set_variable", index=index, source=source, argument=argument
        )
        response = self.nqc.exec_raw(cmd)
        return True if response == b"" else False

    def play_sound(self, sound):
        """Play a sound out of 6 types of sounds."""
        cmd = _verify_and_build_cmd("play_sound", sound=sound)
        response = self.nqc.exec_raw(cmd)
        return True if response == b"" else False

    def play_tone(self, frequency, duration):
        """Play a tone for the duration of x times 1/100 seconds."""
        cmd = _verify_and_build_cmd("play_tone", frequency=frequency, duration=duration)
        response = self.nqc.exec_raw(cmd)
        return True if response == b"" else False

    def set_motor_direction(self, motors, direction):
        """Set direction of motor(s), can be either forward, reverse or flip."""
        cmd = _verify_and_build_cmd("set_motor_direction", code=motors | direction)
        response = self.nqc.exec_raw(cmd)
        return True if response == b"" else False

    def set_motor_state(self, motors, state):
        """Set the state of motor(s), can be either on, off or float."""
        cmd = _verify_and_build_cmd("set_motor_state", code=motors | state)
        response = self.nqc.exec_raw(cmd)
        return True if response == b"" else False

    def set_motor_power(self, motors, source, argument):
        """Set motor power, valid values are 0 to 7."""
        cmd = _verify_and_build_cmd(
            "set_motor_power", motors=motors, source=source, argument=argument
        )
        response = self.nqc.exec_raw(cmd)
        return True if response == b"" else False

    def wait(self, source, argument):
        """Wait the amount of time x * 1/100 (s)."""
        cmd = _verify_and_build_cmd("wait", source=source, argument=argument)
        response = self.nqc.exec_raw(cmd)
        return True if response == b"" else False

    def set_time(self, hours, minutes):
        """Set the device internal clock."""
        cmd = _verify_and_build_cmd("set_time", hours=hours, minutes=minutes)
        response = self.nqc.exec_raw(cmd)
        return True if response == b"" else False
