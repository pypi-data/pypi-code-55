r"""
Marso is a Move Lang parser that supports error recovery and round-trip parsing
for different Python versions (in multiple Python versions). Marso is also able
to list multiple syntax errors in your python file.

Marso has been battle-tested by jedi_. It was pulled out of jedi to be useful
for other projects as well.

Marso consists of a small API to parse Python and analyse the syntax tree.

.. _jedi: https://github.com/davidhalter/jedi

A simple example:

>>> import marso
>>> module = marso.parse('hello + 1', version="3.6")
>>> expr = module.children[0]
>>> expr
PythonNode(arith_expr, [<Name: hello@1,0>, <Operator: +>, <Number: 1>])
>>> print(expr.get_code())
hello + 1
>>> name = expr.children[0]
>>> name
<Name: hello@1,0>
>>> name.end_pos
(1, 5)
>>> expr.end_pos
(1, 9)

To list multiple issues:

>>> grammar = marso.load_grammar()
>>> module = grammar.parse('foo +\nbar\ncontinue')
>>> error1, error2 = grammar.iter_errors(module)
>>> error1.message
'SyntaxError: invalid syntax'
>>> error2.message
"SyntaxError: 'continue' not properly in loop"
"""

from marso.parser import ParserSyntaxError
from marso.grammar import Grammar, load_grammar
from marso.utils import split_lines, python_bytes_to_unicode


__version__ = '0.0.1'


def parse(code=None, **kwargs):
    """
    A utility function to avoid loading grammars.
    Params are documented in :py:meth:`marso.Grammar.parse`.

    :param str version: The version used by :py:func:`marso.load_grammar`.
    """
    version = kwargs.pop('version', None)
    grammar = load_grammar(version=version)
    return grammar.parse(code, **kwargs)
