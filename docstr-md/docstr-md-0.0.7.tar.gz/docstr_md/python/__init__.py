"""# Basic Use"""

from . import compilers
from . import parsers
from .soup_objects import Expr, FunctionDef, ClassDef

from pathlib import PurePath

import ast
import os
import re

_parsers = {'sklearn': parsers.Sklearn}

class PySoup():
    """
    This class parses raw Python code for easy conversion to markdown.

    Parameters
    ----------
    code : str, default=None
        Raw Python code.

    path : str, default=''
        Path to python file. One of `code` or `path` must be specified.

    parser : callable or str, default='sklearn'
        If input as a string, `PySoup` uses it as a key to look up a built-in 
        parser. The parser takes a raw docstring and returns a `docstr` 
        dictionary.

    Attributes
    ----------
    objects : list
        List of soup objects; expressions (`Expr`), functions (`FunctionDef`), 
        classes (`ClassDef`) or string. Strings are usually interpreted as raw 
        markdown.

    parser : callable
        The input `parser`.

    import_path : str
        Import path for soup objects. Setting the import path for the soup automatically sets the import path for its `objects`.

    src_path : str
        Path to the file in the source code repository (e.g. Github). 
        Setting the source code path for the soup automatically sets the 
        source code path for its `objects`.

    src_href : callable
        The `src_href` takes a soup object (`FunctionDef` or `ClassDef`) 
        and converts it to a link to the source code. Setting the 
        `src_href` for the soup automatically sets the `src_href` attribute 
        for its `objects`.

    Examples
    --------
    Create a python file with [parseable docstrings](../../python/parsers). 

    ```python
    from docstr_md.python import PySoup

    # replace with the appropriate file path and docstring parser
    soup = PySoup(path='path/to/file.py', parser='sklearn')
    ```
    """
    def __init__(self, code=None, path='', parser='sklearn', src_href=None):
        assert (code is None) != (path==''), 'Initialize with code xor path.'
        code = code if not path else open(path, 'r').read()
        if isinstance(parser, str):
            parser = _parsers[parser]()
        self.parser = parser
        self._get_objects(code)
        self.import_path = path
        self.src_path = path
        self.src_href = src_href

    def _get_objects(self, code):
        """
        Get objects from raw code as string. Objects of interest are 
        docstrings (expressions), functions, and classes. Excludes private 
        objects, indicated by names starting with '_'.

        Parameters
        ----------
        code : str
            Raw python code
        """
        body = ast.parse(code).body
        self.objects = [
            self.convert_ast_object(obj) for obj in body
            if isinstance(obj, (ast.Expr, ast.FunctionDef, ast.ClassDef))
            and (not hasattr(obj, 'name') or not obj.name.startswith('_'))
        ]

    @property
    def import_path(self):
        return self._import_path

    @import_path.setter
    def import_path(self, path):
        path = re.sub(r'__init__.py$', '', path)
        if path:
            path = '.'.join(PurePath(os.path.splitext(path)[0]).parts)+'.'
        self._setattr('import_path', path)

    @property
    def src_path(self):
        return self._src_path

    @src_path.setter
    def src_path(self, path):
        self._setattr('src_path', path)

    @property
    def src_href(self):
        return self._src_href

    @src_href.setter
    def src_href(self, src_href):
        self._setattr('src_href', src_href)

    def _setattr(self, attr_name, val):
        setattr(self, '_'+attr_name, val)
        [
            setattr(obj, attr_name, val) 
            for obj in self.objects if hasattr(obj, attr_name)
        ]

    def convert_ast_object(self, obj):
        """
        Convert an `ast` object to a soup object.

        Parameters
        ----------
        obj : ast.Expr, ast.FunctionDef, or ast.ClassDef
            `ast` object to convert.

        Returns
        -------
        soup_object : Expr, FunctionDef, or ClassDef
            Specified in docstr_md/python/soup_objects.py.
        """
        if isinstance(obj, ast.Expr):
            return Expr(obj, self.parser)
        elif isinstance(obj, ast.FunctionDef):
            return FunctionDef(obj, self.parser)
        elif isinstance(obj, ast.ClassDef):
            return ClassDef(obj, self.parser)
        raise ValueError('obj type not recognized: ', str(obj))

    def rm_properties(self):
        """
        Remove methods with getter, setter, and deleter decorators from all 
        `ClassDef` soup objects in the `objects` list.

        Returns
        -------
        self : docstr_md.python.PySoup

        Examples
        --------
        Create a python file with a class with methods decorated with 
        `@property`, `@x.setter`, or `@x.deleter`. 

        ```python
        from docstr_md.python import PySoup

        soup = PySoup(path='path/to/file.py', parser='sklearn')
        soup.rm_properties()
        ```

        The `ClassDef` soup objects' `methods` will no longer include 
        properties.
        """
        [
            obj.rm_properties() 
            for obj in self.objects if isinstance(obj, ClassDef)
        ]
        return self



_compilers = {'sklearn': compilers.Sklearn}

def compile_md(soup, compiler='sklearn', outfile=None):
    """
    Compile markdown from a `PySoup` object.

    Parameters
    ----------
    soup : PySoup
        Soup object to convert to markdown.

    compiler : callable or str, default='sklearn'
        If input as a string, it `compiler` is used as a key to look up a 
        built-in compiler. The compiler takes the `soup` and returns a string 
        in markdown format.

    outfile : str or None
        File to which to write the markdown.

    Returns
    -------
    markdown : str
        Markdown formatted as output by the `compiler`.

    Examples
    --------
    Create a python file with [parseable docstrings](../../python/parsers).

    ```python
    from docstr_md.python import PySoup, compile_md

    # replace with the appropriate file path and parser
    soup = PySoup(path='path/to/file.py', parser='sklearn')
    # replace with your desired compiler and output file path
    compile_md(soup, compiler='sklearn', outfile='path/to/outfile.md')
    ```

    You can find the compiled markdown file in `test.md`.
    """
    if isinstance(compiler, str):
        compiler = _compilers[compiler]()
    md = compiler(soup)
    if outfile is not None:
        with open(outfile, 'w') as f:
            f.write(md)
    return md