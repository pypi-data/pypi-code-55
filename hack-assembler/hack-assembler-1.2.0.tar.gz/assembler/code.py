import sys
import logging
from assembler.utils import write_code

from assembler.symbols import get_symbol_table, comp_table, dest_table, jump_table

_log = logging.getLogger(name=__name__)
HACK_FILE_EXTENSION = '.hack'


def _a_instruction(instruction, symbol_table):
    address = instruction['obj'].group(1)

    _log.debug(f"Produce @{address} code")
    try:
        address = int(address)
        return '{0:016b}'.format(address)
    except ValueError:
        address = symbol_table[address]
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


def assemble(parsed_code, file, dry_run):
    symbol_table = get_symbol_table(parsed_code)

    assembled_code = list()
    for instruction in parsed_code:
        if instruction['type'] == 'A_INSTRUCTION':
            assembled_code.append(str(_a_instruction(instruction, symbol_table)))
        elif instruction['type'] == 'C_INSTRUCTION':
            assembled_code.append(str(_c_instruction(instruction)))

    if not dry_run:
        write_code(assembled_code, file)

    return assembled_code
