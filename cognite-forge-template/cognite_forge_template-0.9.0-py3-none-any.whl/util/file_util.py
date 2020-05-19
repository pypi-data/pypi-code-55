import base64
import os
import posixpath
import re
import shutil
from typing import Dict, List, Optional, Tuple, Union

import toml
from cerberus import Validator
from ruamel.yaml import YAML, sys

from forge_template.exception.exceptions import ValidationException


def copy_folders(src: str, dest: str, ignore: Union[List[str], str] = "", overwrite: bool = False) -> None:
    if overwrite or not os.path.exists(dest):
        if ignore:
            if isinstance(ignore, str):
                ignore = [ignore]
            shutil.copytree(src, dest, ignore=shutil.ignore_patterns(*ignore))
        else:
            shutil.copytree(src, dest)


def prepare_rel_posix_path(path: str) -> str:
    """
        Prepare any path in posix format and remove first slash if present
    """
    split_path = re.split(r"\\{1,}|/{1,}", path)
    remove_empty_path = list(filter(None, split_path))
    posix_path = "/".join(remove_empty_path)

    return posix_path


def get_absolute_posix_path(prefix: str, suffix: str = "") -> str:
    prefix = prepare_rel_posix_path(prefix)
    prefix = posixpath.join(posixpath.sep, prefix)
    suffix = prepare_rel_posix_path(suffix)

    return posixpath.join(prefix, suffix)


def copy_files_and_replace_placeholders(src_dest_pairs: List[Tuple[str, str]], placeholder: str, replacement: str):
    for src, dest in src_dest_pairs:
        with open(src, "r") as f:
            content = f.read()

        content = content.replace(placeholder, replacement)
        with open(dest, "w") as f:
            f.write(content)


def get_base64_encoded_content(file_path: str) -> str:
    with open(file_path, "rb") as f:
        content = f.read()
        encoded_content = base64.b64encode(content).decode()

        return encoded_content


def load_yaml(path: str) -> Dict:
    yaml = YAML(typ="safe")
    with open(path, encoding="utf-8") as f:
        dct = yaml.load(f)
        assert isinstance(dct, dict), f"YAML malformatted, couldn't load into dict (got {type(dct)})"
        return dct


def load_toml(path: str) -> Dict:
    with open(path, encoding="utf-8") as f:
        dct = toml.load(f)
        assert isinstance(dct, Dict), f"TOML malformatted, coldn't load into dict (got {type(dct)}"
        return dct


def save_yaml(path: str, content: Dict) -> None:
    yaml = YAML(typ="safe")
    yaml.indent(sequence=4, offset=2)
    with open(path, "w") as f:
        yaml.dump(content, f)


def save_toml(path: str, content: Dict) -> None:
    with open(path, "w") as f:
        toml.dump(content, f)


def dump_yaml_to_stdout(content: Dict) -> None:
    yaml = YAML()
    yaml.indent(sequence=4, offset=2)
    yaml.dump(content, sys.stdout)


def dump_toml_to_stdout(content: Dict) -> None:
    print(toml.dumps(content))


def validate_yaml(schema_path: str, document: Dict) -> Tuple[bool, Optional[Dict]]:
    schema = load_yaml(schema_path)
    validator = Validator(schema)
    return validator.validate(document), validator.errors or None


def load_and_validate_yaml(path: str, schema_path: str) -> Dict:
    loaded_yaml = load_yaml(path)
    is_valid, errors = validate_yaml(schema_path, loaded_yaml)
    if not is_valid:
        raise ValidationException(f"Validation of {path} failed.\n{errors}")
    return loaded_yaml


def read_file(path: str) -> str:
    with open(path, "r", encoding="utf-8") as f:
        return f.read()


def write_file(path: str, content: str) -> None:
    with open(path, "w") as f:
        f.write(content)


def folder_structure_to_dict(path: str) -> Dict:
    paths, names, fnames = [], [], []
    for d, dn, f in os.walk("."):
        paths.append(d)
        names.append(dn)
        fnames.append(f)
    return {}
