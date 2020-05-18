import os

def write_basic_yaml():
    return {
        "DIRECTORY": '',
        "WAVE LENGTHS": [None],
        "RMS": False,
    }

def write_yaml():
    return {
        "BASELINE DIRECTORY": "",
        "DIRECTORY": "",
        "WAVE LENGTHS": [None, None, None, None],
        "GRADIENTS": [10],
        # "RMS": False, TODO: Support RMS
        "ISOTHERMS": [190, 220, 350],
        "TECHNIQUES": {"STA": True, "IR": True, "GC": False, "MS": True},
    }

