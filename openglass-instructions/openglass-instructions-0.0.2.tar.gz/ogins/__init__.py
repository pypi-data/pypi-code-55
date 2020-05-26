class ArgumentType:
    def __init__(self, name, length):
        self.name = name
        self.length = length


PTR = ArgumentType('ptr', 4)
BYTE = ArgumentType('byte', 1)
INT = ArgumentType('int', 2)
LONG = ArgumentType('long', 4)


class Argument:
    def __init__(self, name, type):
        self.type = type
        self.name = name


class Instruction:
    def __init__(self, name, opcode, args):
        self.name = name
        self.opcode = opcode
        self.args = args


POK = Instruction(
        'POK',
        0x00,
        [
            Argument('value', BYTE),
            Argument('location', PTR)
        ]
    )

LON = Instruction(
        'LON',
        0x01,
        []
    )

DEL = Instruction(
        'DEL',
        0x02,
        [
            Argument('time', LONG),
        ]
    )

LOF = Instruction(
        'LOF',
        0x03,
        []
    )

JMP = Instruction(
        'JMP',
        0x04,
        [
            Argument('location', PTR),
        ]
    )

ADB = Instruction(
        'ADB',
        0x05,
        [
            Argument('location', PTR),
            Argument('value', BYTE),
        ]
    )

JEB = Instruction(
        'JEB',
        0x08,
        [
            Argument('target', PTR),
            Argument('check', PTR),
            Argument('value', BYTE),
        ]
    )

SCW = Instruction(
        'SCW',
        0x0E,
        [
            Argument('x', BYTE),
            Argument('y', BYTE)
        ]
    )

SCB = Instruction(
        'SCB',
        0x0F,
        [
            Argument('x', BYTE),
            Argument('y', BYTE)
        ]
    )

HLT = Instruction(
        'HLT',
        0x10,
        [
        ]
    )

SCF = Instruction(
        'SCF',
        0x11,
        [
        ]
    )

instructions = {
        0x00: POK,
        0x01: LON,
        0x02: DEL,
        0x03: LOF,
        0x04: JMP,
        0x05: ADB,
        0x08: JEB,
        0x0E: SCW,
        0x0F: SCB,
        0x10: HLT,
        0x11: SCF,
}
