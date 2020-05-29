import typer as tp
import os.path as path
import random
import castor.attributed_str as NSAttributeDict
from rich import print as rp

cli = tp.Typer()


@cli.command("list")
def ll(filename: str):
    assert path.isfile(filename), \
        f"[ERROR] {filename} is not a file!"
    with open(filename, 'r') as fp:
        lines = fp.readlines()
        print(f"{filename} Total lines {len(lines)}")
        print('====================Sample=========================')
        indexes = random.choices([i for i in range(len(lines))], k=10)
        for i in indexes:
            line_text = NSAttributeDict.bold(f"Line {i}")
            rp(f"{line_text}\t{lines[i]}")
