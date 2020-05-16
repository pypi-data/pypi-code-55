import os.path
import sys

from antlr4 import *

from SpecularLang.SpecLangLexer import SpecLangLexer
from SpecularLang.SpecLangParser import SpecLangParser
from SpecularLang.SpecLangWalker import SpecLangWalker
import argparse


def main():
    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument('file_to_compile', help='The file you want to compile')
    arg_parser.add_argument('-t', '--talkative', type=int, choices=[0, 1], default=1, help='How talkative should Slang be while compiling (0 = Quiet/Errors Only, 1 = Outputs)')
    arg_parser.add_argument('-s', '--scenes', nargs='+', help='The specific scenes to compile')
    arg_parser.add_argument('-o', '--output', type=str, default=os.getcwd(), help='The directory to place the compiled files')
    args = arg_parser.parse_args()
    if not os.path.isfile(os.path.normpath(args.file_to_compile)):
        print("The file you specified doesn't exist.")
    else:
        input_stream = FileStream(args.file_to_compile)
        lexer = SpecLangLexer(input_stream)
        stream = CommonTokenStream(lexer)
        parser = SpecLangParser(stream)
        tree = parser.program()
        if not os.path.exists(args.output):
            print("No directory found with name: {}\n"
                  "If your directory path has spaces in it, surround it in quotes!".format(args.output))
            return
        elif not os.path.isdir(args.output):
            print("Output must be a directory")
            return
        else:
            visitor = SpecLangWalker(os.path.normpath(args.output), args.scenes)
        visitor.visit(tree)


if __name__ == '__main__':
    main()
