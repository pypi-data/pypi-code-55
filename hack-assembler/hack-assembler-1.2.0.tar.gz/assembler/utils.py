from logging import getLogger
from sys import exit
from os.path import realpath, splitext


_log = getLogger(name=__name__)
HACK_FILE_EXTENSION = '.hack'


def get_code(asm_file):
    """
    Reads asm file and constructs list of instruction
    :param asm_file: asm file name
    :return: List of strings represent instruction
    """
    asm_file_path = realpath(asm_file)
    dirty_code = list()
    try:
        with open(asm_file_path, "r") as assembly_file_descriptor:
            _log.debug(f"Start to process {asm_file_path}")
            instruction = assembly_file_descriptor.readline()
            while instruction:
                dirty_code.append(instruction)
                instruction = assembly_file_descriptor.readline()

        return dirty_code
    except FileNotFoundError:
        exit(f"File {asm_file_path} not found.")


def write_code(assembled_code, file):
    """
    Write binary code to hack file
    :param assembled_code: Binary code list
    :param file: Original asm file name
    :return: None
    """
    hack_file = realpath(file)
    hack_file = splitext(hack_file)[0] + HACK_FILE_EXTENSION

    _log.debug(f"Write code to {hack_file}")
    with open(hack_file, "w") as hack_file_descriptor:
        for instruction in assembled_code:
            hack_file_descriptor.write(f"{instruction}\n")
