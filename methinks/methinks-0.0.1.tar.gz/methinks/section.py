import re


# Match sections from a methinks entry
# A title is any markdown style header h1
# Content is any text included on the next line after header
# Until you meet next header or end of file (\Z)
# (?P<name>...) Captures content in parentheses as attr name
# (?=...) Is a lookahead that checks content but doesn't consume input
RE_SPLIT_SECTIONS = r'(?P<section>^#(?P<title>[^#]*?)\n(?P<content>.*?))(?=^#[^#]|\Z)'
RE_TITLE_CONTENT = r'(?P<title>^#+.*?)\n(?P<content>.*)'


class Section(object):
    """A section in a methinks journal entry"""
    def __init__(self):
        super().__init__()

    def propagate(self):
        raise NotImplementedError()

    @classmethod
    def default_text(cl, title):
        """Set a default return, for the first time an entry is instatiated"""
        return "#%s\n" % title

    @classmethod
    def from_text(cl, text):
        """Propagate to next entry"""
        raise NotImplementedError()


class PersistentSection(Section):
    """A section that propagates along time unaltered"""
    def __init__(self, text):
        super().__init__()
        self.text = text

    def propagate(self):
        return self.text

    @classmethod
    def default_text(cl, title):
        header = super().default_text(title)
        note = 'this will persist in next entries until you delete it'
        body = '<your text about %s here> - %s' % (title, note)
        return '%s\n%s\n' % (header, body)

    @classmethod
    def from_text(cl, text):
        return cl(text)


class VolatileSection(Section):
    """A section that drops its contents (applies to single timestep)"""

    def __init__(self, title, content):
        super().__init__()
        self.title = title
        self.content = content

    def propagate(self):
        return '%s\n' % self.title

    @classmethod
    def default_text(cl, title):
        header = super().default_text(title)
        note = 'this will not persist tomorrow - but will be kept in history'
        body = '<your text about %s here> - %s' % (title, note)
        return '%s\n%s\n' % (header, body)

    @classmethod
    def from_text(cl, text):
        regex = re.compile(RE_TITLE_CONTENT, re.MULTILINE | re.DOTALL)
        match = next(regex.finditer(text))
        title, content = match['title'], match['content']
        return cl(title, content)


class TodosSection(Section):
    """A section including todos as [ ] style lists"""

    RE_TODO = r'(?P<todo>[-+*]?\s*?\[ \].*?)(?=([-+*]?\s*?\[x?\]|\Z))'

    def __init__(self, title, todos):
        super().__init__()
        self.title = title
        self.todos = todos

    def propagate(self):
        todo_str = ''.join(self.todos)
        return '%s\n%s' % (self.title, todo_str)

    @classmethod
    def default_text(cl, title):
        header = super().default_text(title)
        examples = ["* [ ] An example incomplete item (will be carried over).",
                    "* [x] An example completed item (will be dropped tomorrow)."]
        return '%s%s\n' % (header, '\n'.join(examples))

    @classmethod
    def from_text(cl, text):
        regex = re.compile(RE_TITLE_CONTENT, re.MULTILINE | re.DOTALL)
        match = next(regex.finditer(text))
        todo_regex = re.compile(cl.RE_TODO, re.MULTILINE | re.DOTALL)
        title, content = match['title'], match['content']
        todos = [m['todo'] for m in todo_regex.finditer(content)]
        return cl(title, todos)
