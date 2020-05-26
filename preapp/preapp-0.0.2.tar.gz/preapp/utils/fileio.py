import os
import json
from typing import Dict, Any, List

__assets_directory__: str = f"{os.path.split(os.path.abspath(__file__))[0]}/../assets"


def file_to_json(file_path: str) -> Dict[str, Any]:
    fp = open(file_path, "r")
    raw_json: Dict[str, Any] = json.load(fp)
    fp.close()
    return raw_json


def raw_to_json_file(file_path: str, raw_json: Dict[str, Any]) -> None:
    fp: TextIOWrapper = open(file_path, "w+")
    json.dump(raw_json, fp, indent=4)
    fp.close()


def str_to_json_file(file_path: str, raw_json: str) -> None:
    raw_to_json_file(file_path, json.loads(raw_json))


def copy_file(src_file: str, dest_file: str) -> None:
    src_fp: TextIOWrapper = open(src_file, "r")
    dest_fp: TextIOWrapper = open(dest_file, "w")
    dest_fp.write("".join(src_fp.readlines()))
    src_fp.close()
    dest_fp.close()


def file_to_text(file_path: str) -> str:
    fp: TextIOWrapper = open(file_path, "r")
    source: str = "".join(fp.readlines())
    fp.close()
    return source


def text_to_file(text: str, file_path: str) -> None:
    fp: TextIOWrapper = open(file_path, "w")
    fp.write(text)
    fp.close()


def get_all_assets(
    directory: str,
    file_type: str = None,
    include_file_extension: bool = True,
    include_full_path: bool = True,
) -> List[str]:
    files: List[str] = [
        f
        for f in os.listdir(f"{__assets_directory__}/{directory}")
        if os.path.isfile(os.path.join(f"{__assets_directory__}/{directory}", f))
    ]

    if file_type != None:
        files = list(filter(lambda f: f.endswith(file_type), files))

    if include_full_path:
        files = list(map(lambda f: f"{__assets_directory__}/{directory}/{f}", files))

    if not include_file_extension:
        files = list(map(lambda f: f.partition(".")[0], files))

    return files
