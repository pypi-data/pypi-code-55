from pathlib import Path
import configparser
from tkinter.filedialog import askdirectory
from tkinter import Tk
import shutil
import errno
import sys

Tk().withdraw()


class Configuration:
    def __init__(self):
        self.user_config_dir = Path.home() / 'ViteezyTool'
        self.config_path = self.user_config_dir / 'config.ini'
        self.ROOT = Path(__file__).resolve().parent.parent
        self.sys_resources = self.ROOT / 'resources'
        config = configparser.ConfigParser()
        if self.config_path.is_file():
            # Found a user config, lets try to load it!
            config.read(self.config_path.absolute().as_posix())
            self.RESOURCES = self.user_config_dir
        else:
            self.first_run()
            config.read((self.sys_resources / 'config.ini').absolute().as_posix())
            self.RESOURCES = self.sys_resources
        self.C_KEY = config["default"]["customer column"]
        self.SHEET = config["default"]["sheet"]
        self.F_NAME = config["default"]["voornaam"]
        self.L_NAME = config["default"]["achternaam"]
        self.PILL_COLUMNS = [config["paklijst kolommen"]['order nummer'], config["paklijst kolommen"]['vitamines'],
                             config["paklijst kolommen"]['stuks']]
        self.MAX_TABLE_HEIGHT = float(config["default"]["max_table_height"])
        self.MAX_IMG_HEIGHT = float(config["default"]["max_img_height"])

        self.IMG = self.RESOURCES / 'img'

    @staticmethod
    def _set_resources(original, config):
        resources_dir = askdirectory(title="Please select a destination folder")
        copyanything(original, resources_dir)
        config.set('default', 'first_run', '0')
        config.set('default', 'resources', resources_dir)
        with open((original / 'config.ini').absolute().as_posix(), 'w') as cfg:
            config.write(cfg)

    def first_run(self):
        print("Hello, it looks like this is your first time running the ViteezyTool")
        print("Before we get started, lets set up a couple of things.")
        print("I will create a resources/configuration folder for you in your home directory.")
        print("Enter 'y' or 'n' to quit or enter 'test' to run a test using the default config")
        response = input(">> ")
        if response == 'n':
            sys.exit()
        elif response == 'y':
            copyanything(self.sys_resources, self.user_config_dir.absolute().as_posix())
            print("Successfully copied the default configuration, I will quit now so that you can edit")
            print("You will find it at {0}".format(self.user_config_dir))
            sys.exit()
        elif response == 'test':
            print("I will now run using the default test configuration")


def copyanything(src, dst):
    try:
        shutil.copytree(src, dst)
    except OSError as exc:  # python >2.5
        if exc.errno == errno.ENOTDIR:
            shutil.copy(src, dst)
        else:
            raise


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


cfg = Configuration()
