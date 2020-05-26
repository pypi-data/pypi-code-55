from muscad import Union


def stack(*parts, overlap=0.01):
    """
    Stack each part on top of each other
    :param parts: all parts
    :param overlap: separation between each part (positive value: pieces will overlap, negative value: pieces will be separated)
    :return: parts stacked on top of each other, bottom to top
    """
    s = Union()
    top = 0
    for part in parts:
        s.add_child(part.align(bottom=top - overlap))
        top = s.top
    return s
