from IPython.display import display, HTML
from .output import displayit

def style(noscroll=True, fullimg=True):
    noscroll and disable_scroll()
    fullimg and full_width_img()

def disable_scroll(selector='.output_scroll', display=True):
    return add_styles('''
        %s {
            height: unset !important;
            border-radius: unset !important;
            -webkit-box-shadow: unset !important;
            box-shadow: unset !important;
        }
    ''' % selector, display=display)

UNSET = 'unset !important'
FORCE = lambda x: '{} !important'.format(x)

def full_width_img(selector='.jp-RenderedImage img', display=True):
    return add_styles(dict2css(selector, width='100%'), display=display)

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
