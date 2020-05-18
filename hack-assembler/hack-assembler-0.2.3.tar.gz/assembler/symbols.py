import logging

_log = logging.getLogger(name=__name__)

comp_table = {
    "0": "0101010",
    "1": "0111111",
    "-1": "0111010",
    "D": "0001100",
    "A": "0110000",
    "!D": "0001101",
    "!A": "0110001",
    "-D": "0001111",
    "-A": "0110011",
    "D+1": "0011111",
    "A+1": "0110111",
    "D-1": "0001110",
    "A-1": "0110010",
    "D+A": "0000010",
    "D-A": "0010011",
    "A-D": "0000111",
    "D&A": "0000000",
    "D|A": "0010101",
    "M": "1110000",
    "!M": "1110001",
    "-M": "1110011",
    "M+1": "1110111",
    "M-1": "1110010",
    "D+M": "1000010",
    "D-M": "1010011",
    "M-D": "1000111",
    "D&M": "1000000",
    "D|M": "1010101"
}

dest_table = {
    "M": "001",
    "D": "010",
    "MD": "011",
    "A": "100",
    "AM": "101",
    "AD": "110",
    "AMD": "111"
}

jump_table = {
    "JGT": "001",
    "JEQ": "010",
    "JGE": "011",
    "JLT": "100",
    "JNE": "101",
    "JLE": "110",
    "JMP": "111"
}

VARIABLES_START_ADDRESS = 16
default_symbols_table = {
    "SP": 0,
    "LCL": 1,
    "ARG": 2,
    "THIS": 3,
    "THAT": 4,
    "R0": 0,
    "R1": 1,
    "R2": 2,
    "R3": 3,
    "R4": 4,
    "R5": 5,
    "R6": 6,
    "R7": 7,
    "R8": 8,
    "R9": 9,
    "R10": 10,
    "R11": 11,
    "R12": 12,
    "R13": 13,
    "R14": 14,
    "R15": 15,
    "SCREEN": 16385,
    "KBD": 24576
}


def get_tables(parsed_code):
    # Get list of label symbols
    label_instructions = list(filter(lambda instruction: instruction['type'] == 'L_INSTRUCTION', parsed_code))
    label_symbols = [instruction['obj'].group(1) for instruction in label_instructions]
    _log.debug(f"Labels in code: {label_symbols}")

    # Build label and variable tables
    assembled_with_symbols_code = list()
    labels_symbols_table = dict(default_symbols_table)
    variables_symbols_table = dict()
    current_address = 0
    for instruction in parsed_code:
        if instruction['type'] == 'A_INSTRUCTION':
            assembled_with_symbols_code.append(instruction)
            variable_symbol = instruction['obj'].group(1)
            # Get first occurrence of variable and assign address from RAM
            if variable_symbol not in label_symbols \
                    and not variable_symbol.isdigit() \
                    and variable_symbol not in default_symbols_table \
                    and variable_symbol not in variables_symbols_table:
                variables_symbols_table[variable_symbol] = len(variables_symbols_table) + VARIABLES_START_ADDRESS
        elif instruction['type'] == 'C_INSTRUCTION':
            assembled_with_symbols_code.append(instruction)
        elif instruction['type'] == 'L_INSTRUCTION':
            label = instruction['obj'].group(1)
            _log.debug(f"Set address of {label} to {current_address}")
            labels_symbols_table[label] = current_address

        current_address = len(assembled_with_symbols_code)

    _log.debug(f"Labels symbols table: {labels_symbols_table}")
    _log.debug(f"Variables symbols table: {variables_symbols_table}")
    return labels_symbols_table, variables_symbols_table
