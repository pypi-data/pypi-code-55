from ..soup_objects import Expr, FunctionDef, ClassDef

from astor import to_source
from markdown import markdown

import os

dir_path = os.path.join(
    os.path.dirname(os.path.realpath(__file__)),
    'sklearn_templates'
)

with open(os.path.join(dir_path, 'head.html'), 'r') as head_f:
    head = head_f.read()
title_template = '##{path}**{name}**'
with open(os.path.join(dir_path, 'header.html'), 'r') as f:
    header_template = f.read()
with open(os.path.join(dir_path, 'table.html'), 'r') as f:
    table_template = f.read()
with open(os.path.join(dir_path, 'field.html'), 'r') as f:
    field_template = f.read()
with open(os.path.join(dir_path, 'item.html'), 'r') as f:
    item_template = f.read()
    
    
class SklearnCompiler():
    """
    Compiles sklearn-style markdown.

    Examples
    --------
    ```python
    from docstr_md.python import PySoup
    from docstr_md.python.compilers import SklearnCompiler

    # replace with the appropriate file path and parser
    soup = PySoup(path='path/to/file.py', parser='sklearn')
    compiler = SklearnCompiler()
    md = compiler(soup)
    ```

    `md` is a string of compiled markdown.
    """
    def __call__(self, soup):
        """
        Compile markdown from soup.

        Parameters
        ----------
        soup : docstr_md.python.PySoup
            Soup to be compiled into markdown.

        Returns
        -------
        md : str
            Compiled markdown.
        """
        return head+'\n\n'.join([self._compile(obj) for obj in soup.objects])
    
    def _compile(self, obj):
        """
        Compile object

        Parameters
        ----------
        obj : soup object or str
            If `obj` is a string, it is treated as raw markdown. Otherwise, 
            the object is compiled depending in its type.

        Returns
        -------
        md : str
            Compiled markdown for the object.
        """
        if isinstance(obj, str):
            return obj
        if isinstance(obj, Expr):
            return self._compile_docstr(obj.docstr)
        if isinstance(obj, FunctionDef):
            return self._compile_func(obj)
        if isinstance(obj, ClassDef):
            return self._compile_cls(obj)
        raise ValueError('Object not recognized:', obj)

    def _compile_docstr(self, docstr):
        """
        Compile a docstring.

        Parameters
        ----------
        docstr : dict
            Parsed docstring dictionary. A dictionary contains a description 
            (str), raw markdown sections (list), and fields (list). Each 
            section is a (name, markdown) tuple. Each field contains a name 
            (str) and items (list). Each item contains a name (str), a short 
            description (usually the data type, str), and a long description 
            (str).

        Returns
        -------
        md : str
            Compiled markdown for the docstring.
        """
        self.docstr = docstr
        return '\n\n'.join([
            docstr['description'],
            self._compile_fields(),
            self._compile_sections(),
        ])
        
    def _compile_cls(self, cls):
        """
        Compile `ClassDef` soup object.

        Parameters
        ----------
        cls : docstr_md.python.soup_objects.ClassDef
            Class object to be compiled.
        """
        return '\n\n'.join([
            self._compile_func(cls.init, cls=cls),
            self._compile_methods(cls.methods),
        ])
        
    def _compile_func(self, func, method=False, cls=None):
        """
        Compile `FunctionDef` soup object.

        Parameters
        ----------
        func : docstr_md.python.soup_objects.FunctionDef
            Function object to be compiled.

        method: bool, default=False
            Indicates that this function is a method of a `ClassDef` object.

        cls : docstr_md.python.soup_objects.ClassDef or None, default=None
            `None` unless this is the `__init__` method. If this is the `__init__` method, `cls` is the Class object to whom the constructor belongs.
        """
        self.func, self.method, self.cls = func, method, cls
        return '\n\n'.join([
            self._compile_title(),
            self._compile_header(),
            self._compile_docstr(func.docstr if cls is None else cls.docstr)
        ])

    def _compile_title(self):
        """Compile the object title."""
        if self.method:
            return ''
        if self.cls is None:
            path = self.func.import_path
            name = self.func.name
        else:
            path = self.cls.import_path
            name = self.cls.name
        return title_template.format(path=path, name=name)
        
    def _compile_header(self):
        """Compile function header."""
        if self.func is None:
            # True when class has no __init__ method
            return ''
        if self.cls is None:
            pfx = '' if self.method else 'def'
            ldelim = '('
            import_path = self.func.import_path
            name = self.func.name
        else:
            pfx = 'class'
            ldelim = '(self, '
            import_path = self.cls.import_path
            name = self.cls.name
        header = to_source(self.func.ast).splitlines()[0]
        args = header.split(ldelim, maxsplit=2)[-1].rsplit(')', maxsplit=2)[0]
        return header_template.format(
            pfx=pfx,
            import_path=import_path,
            name=name,
            args=args
        )
    
    def _compile_fields(self):
        """Compile fields."""
        fields = '\n'.join([
            self._compile_field(field) for field in self.docstr['fields']
        ])
        return table_template.format(fields=fields)
    
    def _compile_field(self, field):
        """Compile a single field."""
        items = '\n'.join(
            [self._compile_item(item) for item in field['items']]
        )
        return field_template.format(name=field['name'], items=items)
    
    def _compile_item(self, item):
        """Compile a single item."""
        item = {key: markdown(val)[3:-4] for key, val in item.items()}
        return item_template.format(**item)
    
    def _compile_sections(self):
        """Compile raw markdown sections."""
        return '\n\n'.join([
            self._compile_section(s) for s in self.docstr['sections']
        ])
    
    def _compile_section(self, section):
        """Compile a single raw markdown section."""
        name_template = '**{}**\n\n' if self.method else '#'*4+'{}\n\n'
        return name_template.format(section[0]) + section[1]
    
    def _compile_methods(self, methods):
        """Compile methods of a `ClassDef` object."""
        if not methods:
            return ''
        return '#'*4+'Methods\n\n'+'\n\n'.join([
            self._compile_func(method, method=True) for method in methods
        ])