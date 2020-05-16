import os.path
import sys

from antlr4 import *

from SpecularLang.SpecLangLexer import SpecLangLexer
from SpecularLang.SpecLangParser import SpecLangParser
from SpecularLang.SpecLangWalker import SpecLangWalker


def main(argv):
    #First arg is the file, second is the output directory
    print(argv)
    if len(argv) < 2:
        print("You must specify a file to compile!")
    elif not os.path.isfile(os.path.normpath(argv[1])):
        print("You must specify a file to compile!")
    else:
        input_stream = FileStream(argv[1])
        lexer = SpecLangLexer(input_stream)
        stream = CommonTokenStream(lexer)
        parser = SpecLangParser(stream)
        tree = parser.program()
        if len(argv) > 2:
            if not os.path.exists(argv[2]):
                print("No directory found with name: {}\n"
                      "If your directory path has spaces in it, surround it in quotes!".format(argv[2]))
                return
            elif not os.path.isdir(argv[2]):
                print("Output must be a directory")
                return
            else:
                visitor = SpecLangWalker(os.path.normpath(argv[2]))
        else:
            print("No output directory specified.\n"
                  "Defaulting to: {}".format(os.getcwd()))
            visitor = SpecLangWalker()
        visitor.visit(tree)


if __name__ == '__main__':
    main(sys.argv)
