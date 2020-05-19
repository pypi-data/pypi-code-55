
from IPython.display import display


class CellDisplay:
    """
    helper class on display()
    see https://stackoverflow.com/questions/60803057/can-i-print-output-to-another-cell-in-a-jupyter-notebook/60931088#60931088
    """

    def __init__(self,
                 name='my-display',
                 max_lines=10):
        self.h = display(display_id=name)
        self.content = ''
        self.mime_type = None
        self.max_lines = max_lines
        self.dic_kind = {
            'text': 'text/plain',
            'markdown': 'text/markdown',
            'html': 'text/html',
        }

    def display(self):
        self.h.display({'text/plain': ''}, raw=True)

    def limit(self, text):
        lines = text.split('\n')
        lines = lines[-self.max_lines:]
        return '\n'.join(lines)

    def _build_obj(self, content, kind, append, new_line):
        self.mime_type = self.dic_kind.get(kind)
        if not self.mime_type:
            return content, False
        if append:
            sep = '\n' if new_line else ''
            self.content = self.limit(self.content + sep + content)
        else:
            self.content = content
        return {self.mime_type: self.content}, True

    def update(self, content, kind=None, append=False, new_line=True):
        obj, raw = self._build_obj(content, kind, append, new_line)
        self.h.update(obj, raw=raw)

    def clear(self):
        self.h.update({'text/plain': ''}, raw=True)

