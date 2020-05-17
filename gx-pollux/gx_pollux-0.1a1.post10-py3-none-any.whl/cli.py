import os, sys
import typer
from pollux.inputer import *
from pollux.license import license_setup, license_text

app = typer.Typer()
types = ['pip', 'tex', 'github']


@app.command()
def init(t: str):
    """
    Init current path as a T type project
    T can be tex, dl
    dl for deep learning
    """
    _t = t.lower()
    _file_names = []
    _dir_names = []
    pwd = os.getcwd()
    os.system("git init")
    if _t == 'tex':
        _file_names = _file_names + ['main.tex', 'ref.bib', 'README.md']
        _dir_names = _dir_names + ['figures', 'chapters']
    elif _t == 'dl':
        _file_names = _file_names + ['train.py', 'main.py', 'model.py',
                                     'README.md', 'config.toml']
        _dir_names = _dir_names + ['layers', 'data', 'dataset']
    _create_dir(pwd, name=_dir_names)
    _create_file(pwd, name=_file_names)


def _create_file(parent, name: list):
    """
    :param parent: parent path
    :param name: file name list
    """
    for f in name:
        filepath = os.path.join(parent, f)
        open(filepath, 'w').close()
        print(f"{filepath} Created!")


def _create_dir(parent, name: list):
    """
    :param parent: parent path
    :param name: file name list
    """
    for p in name:
        dir_path = os.path.join(parent, p)
        os.mkdir(dir_path)
