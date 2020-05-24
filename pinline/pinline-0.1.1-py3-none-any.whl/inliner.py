import ast
import importlib
import inspect
import types


def function_def(function):
    """
    Parameters
    ----------
    function : callable

    Returns
    -------
    function_def : :class:`ast.FunctionDef`
        ast function definition
    """
    try:
        source = inspect.getsource(function)
    except Exception as e:
        ve = ValueError("Error inspecting the source of %s" % function)
        raise ve from e
    else:
        mod = ast.parse(source)

    if not isinstance(mod, ast.Module):
        raise TypeError("ast.parse didn't return a module")

    if len(mod.body) != 1 or not isinstance(mod.body[0], ast.FunctionDef):
        raise TypeError("Module should contain a single function")

    return mod.body[0]


class FunctionVisitor(ast.NodeVisitor):
    def __init__(self, function_def):
        self.function_def = function_def
        signature = function_def.args

        for a in signature.args:
            pass

    def visis_Name(self, node):
        pass

@classmethod
def function_name(cls, function):
    try:
        return function.id
    except AttributeError:
        if isinstance(function, ast.Attribute):
            return function.attr

        return function.name


class InlineTransformer(ast.NodeTransformer):
    """
    """
    def __init__(self, function, inline_functions):
        for fn in inline_functions:
            if not isinstance(fn, ast.FunctionDef):
                raise TypeError("inline_functions must only contain "
                                "ast.FunctionDef objects.")

            if fn.args.vararg:
                raise TypeError("*args aren't currently supported "
                                "in inline function signatures.")

            if fn.args.kwarg:
                raise TypeError("**kwargs aren't currently supported "
                                "in inline function signatures.")

            if fn.args.defaults:
                raise TypeError("keywords aren't currently supported "
                                "in inline function signatures.")

            if getattr(fn, "kwonlyargs", None):
                raise TypeError("keywords aren't currently supported "
                                "in inline function signatures.")



        self.fn = function
        self.inl_fn = {fn.name: fn for fn in inline_functions}

    def visit(self, node):
        for child in ast.iter_child_nodes(node):
            child.parent = node

        return super().visit(node)

    def visit_Call(self, node):
        assert isinstance(node.func, ast.Name)

        print(node.parent)

        if node.func.id in self.inl_fn:
            print("Inlining", node.func.id)

        return node


def inline(*functions):
    def decorator(fn):
        if not all(callable(f) for f in functions):
            raise TypeError("functions must be callable")

        if not callable(fn):
            raise TypeError("%s is not callable" % fn)

        fn_name = fn.__name__

        # Copy namespace of original function's module
        function_mod = importlib.import_module(fn.__module__)
        namespace = dict(inspect.getmembers(function_mod))

        # Get module namespaces of functions to inline
        inline_mods = (f.__module__ for f in functions)
        inline_mods = list(map(importlib.import_module, inline_mods))

        # Update namespace with inlined function's modules
        for inline_mod in inline_mods:
            for k, v in inline_mod.__dict__.items():
                namespace.setdefault(k, v)

        # Get AST's of functions to inline
        inline_asts = list(map(function_def, functions))
        # Get AST of the function to rewrite
        function_ast = function_def(fn)

        InlineTransformer(function_ast, inline_asts).visit(function_ast)

        namespace.pop(fn_name)

        try:
            mod = ast.Module([function_ast], type_ignores=[])
            mod = compile(mod, filename="<ast>", mode="exec")
        except SyntaxError as e:
            raise ValueError("Syntax Error compiling %s" % fn.__name__) from e
        else:
            exec(mod, namespace)

        return namespace[fn_name]

    return decorator

