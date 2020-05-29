import os
import shutil
from typing import List


def makedirs_for_file(filename: str):
    folder = os.path.dirname(filename)
    if folder != "":
        os.makedirs(folder, exist_ok=True)


def copy_mkdir(source: str, destination: str):
    makedirs_for_file(destination)
    shutil.copy(source, destination)


def unlink_files(files: List[str], only_if_exist: bool = True) -> None:
    for file in files:
        if only_if_exist:
            if os.path.isfile(file):
                os.unlink(file)
        else:
            os.unlink(file)


def files_under_folder(folder: str) -> List[str]:
    file_list = []
    for (dir_path, _dir_names, filenames) in os.walk(folder):
        file_list.extend([os.path.join(dir_path, filename) for filename in filenames])
    return file_list


def files_under_folders(folders: List[str]) -> List[str]:
    file_list = []
    for folder in folders:
        file_list.extend(files_under_folder(folder))
    return file_list


def touch(filename: str) -> None:
    with open(filename, "w"):
        pass
