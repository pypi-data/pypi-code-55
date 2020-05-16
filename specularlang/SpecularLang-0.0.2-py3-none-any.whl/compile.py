import sys

from antlr4 import *

from SpecularLang.SpecLangLexer import SpecLangLexer
from SpecularLang.SpecLangParser import SpecLangParser
from SpecularLang.SpecLangWalker import SpecLangWalker


def main(argv):
    input_stream = FileStream(argv[1])
    lexer = SpecLangLexer(input_stream)
    stream = CommonTokenStream(lexer)
    parser = SpecLangParser(stream)
    tree = parser.program()
    if argv[2] is not None:
        visitor = SpecLangWalker(str(argv[2]))
    else:
        visitor = SpecLangWalker()
    visitor.visit(tree)


if __name__ == '__main__':
    main(sys.argv)
