import os

def write_yaml():
    tests = os.path.join(os.getcwd(), "tests")
    return {
        "DIRECTORY": tests,
        "WAVE LENGTHS": [None, None, None, None],
        "GRADIENTS": [30],
        "ISOTHERMS": [30, 60, 90],
        "RMS": False,
        "TECHNIQUES": {"STA": True, "IR": True, "GC": False, "MS": True},
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

