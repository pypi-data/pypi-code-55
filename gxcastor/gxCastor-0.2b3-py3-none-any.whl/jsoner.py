import json
from os import path
import random
import pptree
import rich
import castor.attributed_str as NSAttributedString

type_dict = dict()
type_dict[type(1)] = 'Int'
type_dict[type('hello')] = 'String'
type_dict[type(type_dict)] = 'Dict'
type_dict[type([1, 2, 3])] = 'Array'
type_dict[type(True)] = 'Bool'


def _print_dict(src: dict, level: int = 1):
    global type_dict
    prefix = '    ' * level + '|' + '--' + ' '
    for k, v in src.items():
        print(f"{prefix}Key {k} => valueType-{type_dict[type(v)]}")
        if isinstance(v, dict):
            _print_dict(v, level=level + 1)
        elif isinstance(v, list):
            _print_list(v, level=level + 1)


def _print_list(src: list, k: int = 3, level: int = 1):
    prefix = '    ' * level + '|' + '--' + ' '
    print(f"{prefix}Length {len(src)} Array")
    if isinstance(src[0], dict):
        _print_dict(src[0], level=level + 1)
    elif isinstance(src[0], list):
        _print_list(src, level=level + 1)
    else:
        print(f"{prefix}<Sample {k} items>")
        prefix = '    ' * (level + 1) + '|' + '--' + ' '
        samples = random.choices(src, k=k)
        for i in samples:
            print(f"{prefix}{i}")


class Jsoner:
    def __init__(self,
                 filename: str):
        super(Jsoner, self).__init__()
        self.filename = filename
        self.container = dict()
        self._load()

    def _load(self):
        assert path.isfile(self.filename), f"{self.filename} is not a file"
        self.container = json.load(open(self.filename))

    def printer(self):
        length = 25
        # print(f"{'>' * length}{self.filename}{'>' * length}")
        rich.print(NSAttributedString.bblue(f"{self.filename}{'>' * length}"))
        if isinstance(self.container, dict):
            _print_dict(self.container, level=0)
        elif isinstance(self.container, list):
            _print_list(self.container, level=0)
        rich.print(NSAttributedString.byellow(f"{'<' * length}END{'<' * length}"))

    def print_tree(self):
        if isinstance(self.container, dict):
            root = _tree_print(self.container, rt=self.filename)
        elif isinstance(self.container, list):
            root = _list_tree_print(self.container, name=self.filename)
        pptree.print_tree(root)


def _tree_print(d: dict, rt: str = None, parent: pptree.Node = None):
    if parent is None:
        root = pptree.Node(name=rt, parent=None)
    else:
        root = parent
    for k, v in d.items():
        if isinstance(v, dict):
            k_node = pptree.Node(name=f"[{k}]=>[Dict]", parent=root)
            _tree_print(v, parent=k_node)
        elif isinstance(v, list):
            list_node = pptree.Node(name=f"[{k}]=>[len({len(v)}) Array]", parent=root)
            _list_tree_print(src=v, name=f"[{k}]=>[len({len(v)}) Array]", parent=list_node)
        else:
            print(f"[{k}]=>[{type_dict[type(v)]}]")
            pptree.Node(name=f"[{k}]=>[{type_dict[type(v)]}]", parent=root)
    return root


def _list_tree_print(src: list,
                     k: int = 1,
                     name: str = "[List]",
                     parent: pptree.Node = None) -> pptree.Node:
    children = random.choices(src, k=k)
    if parent is None:
        root = pptree.Node(name=f"[{name}]=>[List]")
    else:
        root = parent
    for child in children:
        if isinstance(child, dict):
            _tree_print(child, rt="[Dict]", parent=root)
        elif isinstance(child, list):
            list_node = pptree.Node(name=f"[len({len(child)}) Array]", parent=root)
            _list_tree_print(child, name="[Array]", parent=list_node)
        else:
            pptree.Node(name=f"[val:{child}]=>[{type_dict[type(child)]}]", parent=root)
    return root
