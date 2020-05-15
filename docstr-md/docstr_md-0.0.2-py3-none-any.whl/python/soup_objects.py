"""#Soup objects

This file defines soup objects. `PySoup` derives soup objects from their `ast` 
equivalents and stores them in its `objects` attribute. These are designed to 
be relatively easy to compile in a markdown file.
"""

from .parsers import SklearnParser

import ast

__all__ = ['Expr', 'FunctionDef', 'ClassDef']

parsers = {'sklearn': SklearnParser}
         

class Expr():
    """
    Stores an expression.

    Parameters
    ----------
    obj : ast.Expr
        Expression object from which this is derived.

    parser : callable or str, default='sklearn'
        If input as a string, `PySoup` uses it as a key to look up a built-in 
        parser. The parser takes a raw docstring and returns a `docstr` 
        dictionary.

    Attributes
    ----------
    ast : ast.Expr
        Original `ast.Expr` object from which this is derived.

    docstr : dict
        Parsed docstring dictionary, output by the `parser`.
    """
    def __init__(self, obj, parser='sklearn'):
        if isinstance(parser, str):
            parser = parsers[parser]()
        self.ast = obj
        self.docstr = parser(obj)
        
        
class Object():
    def __init__(self, obj, parser):
        if isinstance(parser, str):
            parser = parsers[parser]()
        self.ast = obj
        self.name = obj.name
        self.docstr = parser(obj.body[0])
        self.import_path = ''
        

class FunctionDef(Object):
    """
    Stores a function.

    Parameters
    ----------
    obj : ast.FunctionDef
        Function object from which this is derived.

    parser : callable or str, default='sklearn'
        If input as a string, `PySoup` uses it as a key to look up a built-in 
        parser. The parser takes a raw docstring and returns a `docstr` 
        dictionary.

    Attributes
    ----------
    ast : ast.FunctionDef
        Original `ast.FunctionDef` object from which this is derived.

    name : str
        Name of the function.

    docstr : dict
        Parsed docstring dictionary, output by the `parser`.

    import_path : str
        Python formatted import path, e.g. `'path.to.file.'`.
    """
    def __init__(self, obj, parser='sklearn'):
        super().__init__(obj, parser)


class ClassDef(Object):
    """
    Stores a class.

    Parameters
    ----------
    obj : ast.ClassDef
        Class object from which this is derived.

    parser : callable or str, default='sklearn'
        If input as a string, `PySoup` uses it as a key to look up a built-in 
        parser. The parser takes a raw docstring and returns a `docstr` 
        dictionary.

    Attributes
    ----------
    ast : ast.ClassDef
        Original `ast.ClassDef` object from which this is derived.

    name : str
        Name of the class.

    docstr : dict
        Parsed docstring dictionary, output by the `parser`.

    import_path : str
        Python formatted import path, e.g. `'path.to.file.'`.

    methods : list
        List of class methods as `FunctionDef` objects.

    init : docstr_md.python.soup_objects.FunctionDef
        Class constructor.
    """
    def __init__(self, obj, parser='sklearn'):
        super().__init__(obj, parser)
        methods = [
            method 
            for method in obj.body if isinstance(method, ast.FunctionDef)
        ]
        self.methods = [
            FunctionDef(method, parser) for method in methods 
            if (not method.name.startswith('_')) or method.name == '__call__'
        ]
        init = [
            FunctionDef(method, parser) 
            for method in methods if method.name == '__init__'
        ]
        self.init = init[0] if init else None
        