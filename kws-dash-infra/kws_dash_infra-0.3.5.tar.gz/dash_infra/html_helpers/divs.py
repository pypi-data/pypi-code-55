from functools import partial
from uuid import uuid4

from dash_html_components import Div

from . import CustomElement

CustomDiv = CustomElement(Div)

Row = partial(CustomDiv, className="row valign-wrapper")


def Col(s=None, m=None, l=None):
    class_name = f"col"
    if not (s or m or l):
        s = 12

    if s:
        class_name += f" s{s}"

    if m:
        class_name += f" m{m}"

    if l:
        class_name += f" l{l}"

    return partial(CustomDiv, className=class_name)


def Container(*args, **kwargs):
    def wrapper():
        return CustomDiv(*args, **kwargs, className="container", title=str(uuid4()))

    return wrapper
