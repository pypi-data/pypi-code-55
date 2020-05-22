from IPython.display import display
import ipywidgets.widgets as w

def item_title(title=None, *a, **kw):
    return title(*a, **kw) if callable(title) else title

def fake_header(child, title=None, header_size=1, **kw):
    from  .tags import header
    if title:
        child = w.VBox([header(title, header_size), child], **kw)
        child.is_title = True
    return child

def set_tuple(tup, i, item):
    return tup[:i] + (item,) + tup[i+1:]



class _DisplayMixin:
    def display(self):
        return displayit(self)

    @property
    def D(self):
        return self.display()

def displayit(obj, show=True):
    show and display(obj)
    return obj


C = None
def gcw():
    return C

def scw(widget):
    global C
    C = widget
