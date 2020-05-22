from IPython.display import HTML
from .util import displayit

def style(noscroll=True, fullimg=False):
    noscroll and disable_scroll()
    fullimg and full_width_img()

def disable_scroll(selector='.output_scroll', display=True):
    rmkeys = ('height', 'border-radius', '-webkit-box-shadow', 'box-shadow')
    return add_styles(dict2css(selector, {k: UNSET for k in rmkeys}), display=display)

def full_width_img(selector='.jp-RenderedImage img', width='100%', display=True):
    return add_styles(dict2css(selector, width=width), display=display)

UNSET = 'unset !important'
FORCE = '{} !important'.format

def add_styles(styles, display=True):
    return displayit(HTML('''
    <style>
        {}
    </style>
    '''.format(styles)), show=display)

def dict2css(selector, props=None, nindent=2, **kw):
    return '''
        {} {{
            {}
        }}
    '''.format(selector, '\n'.join(
        ' ' * nindent + '{}: {};'.format(k, v)
        for k, v in dict(props or (), **kw).items()
    ))
