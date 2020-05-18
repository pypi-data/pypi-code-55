import sys
import logging
import re
import string
from os.path import realpath as path_realpath

_log = logging.getLogger(name=__name__)

# Regexps for Hack instructions
#
# group(1) of A instruction match returns address or label
#
# group(1) of C instruction match returns destination specification
# group(2) of C instruction match returns computation specification
# group(3) of C instruction match returns jump specification
A_INSTRUCTION = re.compile("^@([0-9]+|[a-zA-Z_.$:]+[0-9a-zA-Z_.$:]*)$")
C_INSTRUCTION = re.compile("^([AMD]=)*([AMD!\-+|&01]+)(;[JGTEQLNMP]*)*$")
L_INSTRUCTION = re.compile("^\(([a-zA-Z_.$:]+[0-9a-zA-Z_.$:])*\)$")
COMMENT = re.compile("//.*")


def _cleanup_instruction(instruction):
    instruction = instruction.translate({ord(whitespace): None for whitespace in string.whitespace})
    return re.sub(COMMENT, "", instruction)


def _instruction_type(instruction):
    if (match_instruction_object := re.fullmatch(A_INSTRUCTION, instruction)) is not None:
        _log.debug(f"{instruction} is A instruction")
        return {"type": "A_INSTRUCTION", "obj": match_instruction_object}
    elif (match_instruction_object := re.fullmatch(C_INSTRUCTION, instruction)) is not None:
        _log.debug(f"{instruction} is C instruction")
        return {"type": "C_INSTRUCTION", "obj": match_instruction_object}
    elif (match_instruction_object := re.fullmatch(L_INSTRUCTION, instruction)) is not None:
        _log.debug(f"{instruction} is L (label) instruction")
        return {"type": "L_INSTRUCTION", "obj": match_instruction_object}
    else:
        raise ValueError(f"{instruction} is unknown")


def parse(asm_file):
    asm_file_path = path_realpath(asm_file)

    parsed_code = list()
    try:
        with open(asm_file_path, "r") as assembly_file_descriptor:
            _log.debug(f"Start to process {asm_file_path}")
            instruction = assembly_file_descriptor.readline()
            while instruction:
                instruction = _cleanup_instruction(instruction)
                if instruction:
                    # If not empty string or comment let's parse it
                    parsed_code.append(_instruction_type(instruction))

                instruction = assembly_file_descriptor.readline()

        return parsed_code
    except FileNotFoundError:
        sys.exit(f"File {asm_file_path} not found.")
