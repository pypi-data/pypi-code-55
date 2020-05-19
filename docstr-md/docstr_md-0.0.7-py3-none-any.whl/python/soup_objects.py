"""# Soup objects

This file defines soup objects. `PySoup` derives soup objects from their `ast` 
equivalents and stores them in its `objects` attribute. These are designed to 
be relatively easy to compile in a markdown file.
"""

from . import parsers

import ast

__all__ = ['Expr', 'FunctionDef', 'ClassDef']

parsers = {'sklearn': parsers.Sklearn}
         

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
        self.import_path = self.src_path = ''
        self.src_href = None
        self.lineno = obj.lineno

    def compile_src_href(self):
        """
        Compile hyperlink ot object source code.
        """
        return '' if self.src_href is None else self.src_href(self)
        

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

    src_path : str
        Path to file in the source code. e.g. `'path/to/file.py'`.

    src_href : callable
        Takes `self` and outputs a link to the this object in the source 
        code repository.
    """
    def __init__(self, obj, parser='sklearn'):
        super().__init__(obj, parser)

    def is_property(self):
        """
        Indicates that this function is a getter, setter, or deleter.

        i.e. This function is a method of a class decorated with 
        `@property`, `@x.setter`, or `@x.deleter`.

        Returns
        -------
        is_property : bool
            Indicator that this function is a property.
        """
        for decorator in self.ast.decorator_list:
            if isinstance(decorator, ast.Name) and decorator.id == 'property':
                return True
            elif isinstance(decorator, ast.Attribute):
                if decorator.attr in ('setter', 'deleter'):
                    return True
        return False


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

    src_path : str
        Path to file in the source code. e.g. `'path/to/file.py'`.

    src_href : callable
        Takes `self` and outputs a link to the this object in the source 
        code repository. Setting the `src_href` for self automatically sets 
        the `src_href` attributes for its `methods`.

    methods : list
        List of class methods as `FunctionDef` objects.

    init : docstr_md.python.soup_objects.FunctionDef
        Class constructor.
    """
    def __init__(self, obj, parser='sklearn'):
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
        super().__init__(obj, parser)
        
    @property
    def src_path(self):
        return self._src_path

    @src_path.setter
    def src_path(self, val):
        self._setattr('src_path', val)

    @property
    def src_href(self):
        return self._src_href

    @src_href.setter
    def src_href(self, val):
        self._setattr('src_href', val)

    def _setattr(self, attr_name, val):
        setattr(self, '_'+attr_name, val)
        [setattr(method, attr_name, val) for method in self.methods]

    def rm_properties(self):
        """
        Remove methods with getter, setter, and deleter decorators.

        Returns
        -------
        self : docstr_md.python.soup_objects.ClassDef
        """
        self.methods = [m for m in self.methods if not m.is_property()]
        return self