from pathlib import Path
import configparser

ROOT = Path(__file__).resolve().parent.parent
IMG = ROOT / 'resources' / 'img'
RESOURCES = ROOT / 'resources'
OUTPUT = ROOT.parent / 'output'
config = configparser.ConfigParser()
config.read((RESOURCES / 'config.ini').absolute().as_posix())
C_KEY = config["default"]["customer column"]
SHEET = config["default"]["sheet"]
F_NAME = config["default"]["voornaam"]
L_NAME = config["default"]["achternaam"]
PILL_COLUMNS = [config["paklijst kolommen"]['order nummer'], config["paklijst kolommen"]['vitamines'],
                config["paklijst kolommen"]['stuks']]
MAX_TABLE_HEIGHT = float(config["default"]["max_table_height"])
MAX_IMG_HEIGHT = float(config["default"]["max_img_height"])


def is_number(s: str):
    """
    Function that checks if s is a number
    :param s: string that may or may not be a number
    :return: true if s is a number
    """
    try:
        float(s)
        return True
    except ValueError:
        return False
