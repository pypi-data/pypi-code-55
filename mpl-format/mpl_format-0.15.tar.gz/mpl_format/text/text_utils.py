from textwrap import wrap
from typing import Union

from matplotlib.text import Text

from mpl_format.settings import MAX_LABEL_WIDTH


def wrap_text(text: Union[str, Text], max_width: int = None) -> str:
    """
    Wrap text that exceeds a given width of characters with new lines.

    :param text: The text to wrap.
    :param max_width: The maximum character width per line.
    """
    max_chars = max_width or MAX_LABEL_WIDTH
    if isinstance(text, str):
        return '\n'.join(wrap(text=text, width=max_chars))
    elif isinstance(text, Text):
        return '\n'.join(wrap(text=text.get_text(), width=max_chars))
    else:
        raise ValueError(f'Cannot wrap text for type {type(text)}.')


def remove_parenthesized_text(text: Union[str, Text]) -> str:
    """
    Remove any text inside parentheses, along with the parentheses.

    :param text: The text to modify.
    """
    if isinstance(text, Text):
        text = text.get_text()

    while '(' in text and ')' in text:
        l_pos = text.index('(')
        r_pos = text.index(')')
        text = text[:l_pos] + text[r_pos + 1:]
    return text
