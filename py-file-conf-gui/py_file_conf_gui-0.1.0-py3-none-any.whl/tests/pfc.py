import os
import shutil
from typing import Callable
from copy import deepcopy

from pyfileconf import PipelineManager

from tests.config import BASE_GENERATED_DIR
from tests.input_files.amodule import a_function
from tests.input_files.mypackage.cmodule import ExampleClass

PM_FOLDER = os.path.join(BASE_GENERATED_DIR, 'pm')
LOGS_PATH = os.path.join(PM_FOLDER, 'MyLogs')
DEFAULTS_FOLDER_NAME = 'defaults'
EXAMPLE_CLASS_FILE_NAME = 'example_class_dict.py'
EXAMPLE_CLASS_FILE_PATH = os.path.join(PM_FOLDER, EXAMPLE_CLASS_FILE_NAME)
EC_CLASS_DICT = {
    'class': ExampleClass,
    'name': 'example_class'
}
CLASS_CONFIG_DICT_LIST = [
    EC_CLASS_DICT
]

PM_DEFAULTS = dict(
    folder=PM_FOLDER,
    name='guipm',
    log_folder=LOGS_PATH,
    default_config_folder_name=DEFAULTS_FOLDER_NAME,
    specific_class_config_dicts=CLASS_CONFIG_DICT_LIST,
)


def full_pm_setup(**kwargs) -> PipelineManager:
    if not os.path.exists(PM_FOLDER):
        os.makedirs(PM_FOLDER)
    write_to_pipeline_dict_file()
    write_example_class_dict_to_file()
    pm = create_pm(**kwargs)
    pm.load()
    return pm


def create_pm(**kwargs) -> PipelineManager:
    all_kwargs = deepcopy(PM_DEFAULTS)
    all_kwargs.update(**kwargs)
    pipeline_manager = PipelineManager(**all_kwargs)
    return pipeline_manager


def delete_pm_project(path: str = PM_FOLDER, logs_path: str = LOGS_PATH):
    all_paths = [
        os.path.join(path, 'defaults'),
        os.path.join(path, 'pipeline_dict.py'),
        logs_path,
    ]
    for path in all_paths:
        if os.path.isdir(path):
            shutil.rmtree(path)
        elif os.path.isfile(path):
            os.remove(path)
        else:
            # Must not exist, maybe add handling for this later
            pass


def write_to_pipeline_dict_file(pm_folder: str = PM_FOLDER, nest_section: bool = True):
    file_path = os.path.join(pm_folder, 'pipeline_dict.py')

    write_str = """
from tests.input_files.amodule import a_function
from tests.input_files.mypackage.cmodule import ExampleClass

pipeline_dict = {
    "my_section": {"stuff": [a_function,], "woo": [ExampleClass,],},
}
"""
    with open(file_path, 'w') as f:
        f.write(write_str)


def class_dict_str(name: str, key: str, value: str) -> str:
    return f'\n{name} = {{\n\t"{key}": ["{value}"],\n}}\n'


def nested_class_dict_str(name: str, section_key: str, key: str, value: str) -> str:
    return f'\n{name} = {{\n\t"{section_key}": {{\n\t\t"{key}": ["{value}"],\n\t}},\n}}\n'


def write_example_class_dict_to_file(nest_section: bool = True):
    if nest_section:
        write_str = nested_class_dict_str('class_dict', 'my_section', 'stuff', 'data')
    else:
        write_str = class_dict_str('class_dict', 'stuff', 'data')
    with open(EXAMPLE_CLASS_FILE_PATH, 'w') as f:
        f.write(write_str)


if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument('-d', '--delete', action='store_true')

    args = parser.parse_args()

    if args.delete:
        delete_pm_project()
    else:
        pm = full_pm_setup()
