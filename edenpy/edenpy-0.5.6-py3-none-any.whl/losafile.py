"""load and save files with various extensions"""

import os.path
import json


def save_json(data, path):
    """save json file

    If the file already exists in the storage path, append data.

    Args:
        data: (list) data to be saved
        path: save path
    """
    if os.path.isfile(path):
        with open(path) as jf:
            new_data = json.load(jf)
            new_data.extend(data)
    else:
        new_data = data

    with open(path, 'w', encoding="utf-8") as jfout:
        json.dump(new_data, jfout, indent="\t", ensure_ascii=False)
