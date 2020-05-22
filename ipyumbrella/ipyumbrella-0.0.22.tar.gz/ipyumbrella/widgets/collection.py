from contextlib import contextmanager
from IPython.display import display as display_
import ipywidgets.widgets as w
from .output import Output
from  .tags import header


class _CollectionMixin:
    output_layout = w.Layout()
    # title_layout = w.Layout(font_size='1.2em')
    def __init__(self, *a, output_layout=None, **kw):
        super().__init__(*a, **kw)
        self.output_layout = output_layout or self.output_layout

    def item(self, title=None, layout=None, err_stop=True, **kw):
        outlayout = w.Layout() if title else layout or self.output_layout
        return self.append(
            Output(err_stop=err_stop, layout=outlayout, **kw),
            title=title, layout=layout)

    def append(self, child, title=None, layout=None, header_size=3):
        if title:
            wrap = w.VBox([header(title, header_size), child],
                          layout=layout or self.output_layout)
            self.children += (wrap,)
        else:
            self.children += (child,)
        return child

    def __len__(self):
        return len(self.children)

    def display(self):
        display_(self)
        return self

    @property
    def D(self):
        return self.display()

    def items(self, items, title=None, **kw):
        for item in items:
            with self.item(title=title(item) if callable(title) else title, **kw):
                yield item

class _SelectableCollectionMixin(_CollectionMixin):
    def item(self, title=None, selected=True, err_stop=True, **kw):
        return self.append(Output(err_stop=err_stop, **kw), title, selected=selected)

    def select(self, i):
        self.selected_index = i

    def append(self, child, title=None, selected=True):
        self.children += (child,)
        title and self.set_title(len(self) - 1, title)
        self.select(selected and len(self) - 1)
        return child


class Carousel(w.Box, _CollectionMixin):
    layout = w.Layout(
        flex_flow='row nowrap',
        overflow_x='auto',
        overflow_y='visible',
        max_width='100%',
    )
    output_layout = w.Layout(min_width='60%')

class Accordion(w.Accordion, _SelectableCollectionMixin):
    pass

class Tab(w.Tab, _SelectableCollectionMixin):
    pass
