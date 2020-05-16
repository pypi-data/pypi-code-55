"""#Basic Use"""

from .compilers import SklearnCompiler
from .parsers import SklearnParser
from .soup_objects import Expr, FunctionDef, ClassDef

from pathlib import PurePath

import ast
import os
import re

parsers = {'sklearn': SklearnParser}

class PySoup():
    """
    `PySoup` parses raw Python code for easy conversion to markdown.

    Parameters
    ----------
    code : str, default=None
        Raw Python code.

    path : str, default=None
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

    Examples
    --------
    Create a python file with [parseable docstrings](../../python/parsers). 

    ```python
    from docstr_md.python import PySoup

    # replace with the appropriate file path and docstring parser
    soup = PySoup(path='path/to/file.py', parser='sklearn')
    ```
    """
    def __init__(self, code=None, path=None, parser='sklearn'):
        assert (code is None) != (path is None), 'Initialize with code xor path.'
        code = code if path is None else open(path, 'r').read()
        if isinstance(parser, str):
            parser = parsers[parser]()
        self.parser = parser
        body = ast.parse(code).body
        self.objects = [
            self.convert_ast_object(obj) for obj in body
            if isinstance(obj, (ast.Expr, ast.FunctionDef, ast.ClassDef))
        ]
        self.set_import_path(path)

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

    def set_import_path(self, path):
        """
        Set the import path for the soup and its `objects`.

        Parameters
        ----------
        path : str
            Path, usually to a .py file.

        Returns
        -------
        None
        """
        path = re.sub(r'__init__.py$', '', path)
        if path:
            path = '.'.join(PurePath(os.path.splitext(path)[0]).parts)+'.'
        self.import_path = path
        [
            setattr(obj, 'import_path', path) for obj in self.objects
            if hasattr(obj, 'import_path')
        ]


compilers = {'sklearn': SklearnCompiler}

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
        compiler = compilers[compiler]()
    md = compiler(soup)
    if outfile is not None:
        with open(outfile, 'w') as f:
            f.write(md)
    return md