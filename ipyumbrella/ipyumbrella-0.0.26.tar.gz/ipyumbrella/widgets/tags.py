from IPython.display import display, HTML
from .output import Output


def h1(content):
    return header(content, 1)

def h2(content):
    return header(content, 1)

def h3(content):
    return header(content, 1)

def h4(content):
    return header(content, 1)

def h5(content):
    return header(content, 1)

def h6(content):
    return header(content, 1)

def header(content, level=1):
    return tag(content, 'h{}'.format(level))

def div(content):
    return tag(content, 'div')

def tag(content, elem='div'):
    out = Output()
    with out:
        display(HTML('<{elem}>{content}</{elem}>'.format(content=content, elem=elem)))
    return out
