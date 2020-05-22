from configparser import ConfigParser
from os import mkdir
from os.path import expanduser, join, exists
import pathlib
from setuptools import find_packages, setup, Extension


HERE = pathlib.Path(__file__).parent
README = (HERE/"README.txt").read_text()

USER_HOME_DIR = expanduser("~")
CML_DIR_NAME = ".conML"
DEFAULT_LEARN_DIR = "data"
CONFIG_FILE_NAME = "settings.ini"
DEFAULT_TRAINING_SET = "toyset.csv"
KNOWLEDGE_DIR = "knowledge"

CML_CONFIG_DIR = join(USER_HOME_DIR, CML_DIR_NAME)
CML_DEFAULT_LEARN_DIR = join(CML_CONFIG_DIR, DEFAULT_LEARN_DIR)
CONFIG_FILE_PATH = join(CML_CONFIG_DIR, CONFIG_FILE_NAME)
DEFAULT_TRAINING_SET_PATH = join(CML_DEFAULT_LEARN_DIR, DEFAULT_TRAINING_SET)
KNOWLEDGE_DIR_PATH = join(CML_CONFIG_DIR, KNOWLEDGE_DIR)


def create_cml_config_dir():
    mkdir(CML_CONFIG_DIR)


def create_data_dir():
    mkdir(CML_DEFAULT_LEARN_DIR)


def insert_default_settings_into_config_file():
    config = ConfigParser()
    config.read(CONFIG_FILE_PATH)
    config["GENERAL"]["input_file"] = DEFAULT_TRAINING_SET_PATH
    config["GENERAL"]["learn_dir"] = CML_DEFAULT_LEARN_DIR
    config["GENERAL"]["knowledge_dir"] = KNOWLEDGE_DIR_PATH
    write_configs(config)


def write_configs(config):
    with open(CONFIG_FILE_PATH, 'w') as configfile:
        config.write(configfile)


if not exists(CML_CONFIG_DIR):
    create_cml_config_dir()


setup(
    name = "conML",
    packages = find_packages(),
    version = 0.32,
    licence="MIT",
    description="constructivist machine learning",
    long_description=README,
    long_description_content_type="text/plain",
    data_files=[(CML_CONFIG_DIR, ["conML/static/settings.ini"]),
                (CML_DEFAULT_LEARN_DIR, ["conML/static/toyset.csv"]),
                ("conML/static", ["conML/static/logging.ini"])],
    author="Dmitrij Denisenko",
    install_requires = [
        "numpy",
        "krippendorff",
        "scikit-learn",
        "scipy",
        "pandas"
    ]
)
