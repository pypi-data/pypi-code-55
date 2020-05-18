import sys
import logging
from os.path import realpath as path_realpath
from os.path import splitext as path_splitext

from assembler.symbols import get_tables, comp_table, dest_table, jump_table

_log = logging.getLogger(name=__name__)
HACK_FILE_EXTENSION = '.hack'


def _a_instruction(instruction, symbol_table, variable_table):
    address = instruction['obj'].group(1)

    _log.debug(f"Produce @{address} code")
    try:
        address = int(address)
        return '{0:016b}'.format(address)
    except ValueError:
        address = symbol_table.get(address, variable_table.get(address))
        address = int(address)
        return '{0:016b}'.format(address)


def _c_instruction(instruction):
    instruction_tuple = instruction['obj'].groups()
    _log.debug(f"Produce {instruction_tuple} code")

    header = "111"
    comp = instruction['obj'].group(2)
    dest = instruction['obj'].group(1)
    jump = instruction['obj'].group(3)

    if comp:
        try:
            comp_field = comp_table[comp]
        except KeyError:
            sys.exit(f"Unknown computation field: {comp}")
    else:
        sys.exit(f"Computation field must be present: {instruction_tuple}")

    if dest:
        try:
            dest_field = dest_table[dest.strip('=')]
        except KeyError:
            sys.exit(f"Unknown destination field: {dest}")
    else:
        dest_field = "000"

    if jump:
        try:
            jump_field = jump_table[jump.strip(';')]
        except KeyError:
            sys.exit(f"Unknown jump field: {dest}")
    else:
        jump_field = "000"

    return header + comp_field + dest_field + jump_field


def assemble(parsed_code, file):
    symbol_table, variable_table = get_tables(parsed_code)

    assembled_code = list()
    for instruction in parsed_code:
        if instruction['type'] == 'A_INSTRUCTION':
            assembled_code.append(str(_a_instruction(instruction, symbol_table, variable_table)))
        elif instruction['type'] == 'C_INSTRUCTION':
            assembled_code.append(str(_c_instruction(instruction)))

    hack_file = path_realpath(file)
    hack_file = path_splitext(hack_file)[0] + HACK_FILE_EXTENSION

    _log.debug(f"Write code to {hack_file}")
    with open(hack_file, "w") as hack_file_descriptor:
        for instruction in assembled_code:
            hack_file_descriptor.write(f"{instruction}\n")

    return assembled_code
