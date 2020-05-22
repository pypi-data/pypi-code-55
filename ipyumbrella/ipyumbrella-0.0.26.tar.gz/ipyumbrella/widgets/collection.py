from functools import wraps
import ipywidgets.widgets as w
from .output import Output
from . import util

class _CollectionMixin(util._DisplayMixin):
    output_layout = w.Layout()
    def __init__(self, *a, output_layout=None, **kw):
        super().__init__(*a, **kw)
        self.output_layout = output_layout or self.output_layout

    def __len__(self):
        return len(self.children)

    '''Item Creators'''

    def item(self, title=None, layout=None, err_stop=True, selected=True, **kw):
        return self.append(
            Output(err_stop=err_stop, layout=layout or self.output_layout, **kw),
            title=title, selected=selected)

    def items(self, items, title=None, **kw):
        for item in items:
            with self.item(title=util.item_title(title, item), **kw):
                yield item

    def function(self, func, title=None, **kw):
        @wraps(func)
        def inner(*ai, **kwi):
            with self.item(title=util.item_title(title, *ai, **kwi), **kw):
                return func(*ai, **kwi)
        return inner

    def append(self, child, title=None, selected=True, update=True, pos=None):
        pos = (
            pos if pos is not None
            else self._get_pos(title) if update and title
            else len(self.children))

        self.children = util.set_tuple(self.children, pos, child)
        title and self.set_title(pos, title)
        selected and self.select(pos)
        return child

    '''Utils'''

    def _get_pos(self, title):
        return next((
            i for i, c in enumerate(self.children)
            if getattr(c, 'title', None) == title
        ), len(self.children))

    def select(self, i):
        self.selected_index = i

class _FauxTitleMixin:
    def __init__(self, *a, header_size=3, **kw):
        super().__init__(*a, **kw)
        self.header_size = header_size

    def set_title(self, i, title):
        child = self.children[i]
        if getattr(child, 'is_title', False): # remove title
            layout, child = child.layout or self.output_layout, child.children[1]
        else: # replace
            layout, child.layout = self.output_layout, w.Layout()

        self.children = util.set_tuple(self.children, i, util.fake_header(
            child, title, layout=layout, header_size=self.header_size))


class Carousel(w.Box, _CollectionMixin, _FauxTitleMixin):
    layout = w.Layout(
        flex_flow='row nowrap',
        overflow_x='auto',
        overflow_y='visible',
        max_width='100%',
    )
    output_layout = w.Layout(min_width='60%')

class Accordion(w.Accordion, _CollectionMixin):
    pass

class Tab(w.Tab, _CollectionMixin):
    pass
