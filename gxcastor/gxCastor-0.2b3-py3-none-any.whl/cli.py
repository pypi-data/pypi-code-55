import typer
import os.path as path
import random
from rich import print as rp
from castor.attributed_str import bold
import castor.attributed_str
from castor.jsoner import Jsoner

app = typer.Typer()
type_dict = dict()
type_dict[type(1)] = 'Int'
type_dict[type('hello')] = 'String'
type_dict[type(type_dict)] = 'Dict'
type_dict[type([1, 2, 3])] = 'Array'
type_dict[type(True)] = 'Bool'


# display_filename_prefix_middle = '├──'
# display_filename_prefix_last = '└──'
# display_parent_prefix_middle = '    '
# display_parent_prefix_last = '│   '


@app.command()
def json(filename: str, tree: bool = False):
    """
    JSON Visualizer
    """
    assert path.isfile(filename), f"{filename} is no a file"
    jsoner = Jsoner(filename=filename)
    if tree:
        jsoner.print_tree()
    else:
        jsoner.printer()


@app.command()
def text(filename: str,
         k: int = typer.Option(10, '-k'),
         output: int = typer.Option(-1, "--out", '-o')
         ):
    assert path.isfile(filename), \
        f"[ERROR] {filename} is not a file!"
    with open(filename, 'r') as fp:
        lines = fp.readlines()
        print(f"{filename} Total lines {len(lines)}")
        print('====================Sample=========================')
        indexes = random.choices([i for i in range(len(lines))], k=k)
        for i in indexes:
            line_text = bold(f"Line {i}")
            rp(f"{line_text}\t{lines[i]}")
        if output != -1:
            #  output
            indexes = random.choices([i for i in range(len(lines))], k=output)
            sample_file = f"{filename.split('.')[0]}-sample.txt"
            with open(sample_file, 'w') as sp:
                for line in indexes:
                    print(line, file=sp)
            rp(castor.attributed_str.clear(f"{sample_file} Created!"))
