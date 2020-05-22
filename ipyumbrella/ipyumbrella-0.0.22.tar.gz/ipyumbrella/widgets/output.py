from IPython import get_ipython
from IPython.display import display, HTML
import ipywidgets.widgets as w
from traitlets import Bool

class Output(w.Output):
    err_stop = Bool(True, help="Stop execution when exception is raised.").tag(sync=True)

    def __init__(self, no_scroll=True, **kw):
        super().__init__(**kw)
        if no_scroll:
            self.add_class('output_scroll_disabled')

    def __exit__(self, etype, evalue, tb):
        """Called upon exiting output widget context manager."""
        ip = get_ipython()

        # print(type(etype), type(evalue), hasattr(evalue, '__already_shown_by_ipywidgets_output'), evalue.__already_shown_by_ipywidgets_output)
        if etype is not None and not hasattr(evalue, '_already_shown_by_ipywidgets_output'):
            if ip:
                evalue.__already_shown_by_ipywidgets_output = True
                ip.showtraceback((etype, evalue, tb), tb_offset=0)
        self._flush()
        self.msg_id = ''
        # if self.err_stop:
        #     raise ExceptionAlreadyShownByOutput(etype, evalue, tb)
        return not self.err_stop if ip else None


class ShrinkWrap(Output):
    layout = w.Layout(display='flex', overflow_x='auto')

def displayit(obj):
    display(obj)
    return obj

def disable_scroll(selector='.output_scroll'):
    return displayit(disable_scroll_obj(selector))

def disable_scroll_obj(selector='.output_scroll'):
    return HTML('''
    <style>
        %s {
            height: unset !important;
            border-radius: unset !important;
            -webkit-box-shadow: unset !important;
            box-shadow: unset !important;
        }
    </style>
    ''' % selector)

def css(selector, nindent=2, **kw):
    display(HTML('''
    <style>
        {} {{
            {}
        }}
    </style>
    '''.format(selector, '\n'.join(
        ' ' * nindent + '{}: {};'.format(k, v)
        for k, v in kw.items()
    ))))
