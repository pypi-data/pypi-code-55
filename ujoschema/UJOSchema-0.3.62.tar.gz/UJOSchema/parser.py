#
# Copyright (c) 2018-present, wobe-systems GmbH
#
# This source code is licensed under the MIT license found in the
# LICENSE file in the root directory of this source tree.
#

""" parsing of schema files and strings """

import os.path
from lark import Lark


def to_filename_tuple(filename_or_dir, extensions):
    """
    Get all filenames from a directory as a tuple.
    """
    path = filename_or_dir
    if not os.path.isdir(path):
        files = (path,)
    else:
        files = (
            os.path.join(path, f) for f in os.listdir(path) if f.endswith(extensions)
        )
    return files


class UjsParser:
    """
    Create a parse tree for ujs files
    """

    def __init__(
        self,
        grammar_file_or_folder=os.path.join(os.path.dirname(__file__), "grammar"),
        start="start",
    ):
        grammar = self.get_grammar(grammar_file_or_folder)
        self._parser = Lark(grammar, parser="lalr", start=start)

    def parse_file(self, filename):
        """
        Load code from a textfile and return a parse tree.

        Parameter:
            filename : [string] path and filename of the source

        Return:
            [lark.tree] parse tree
        """
        with open(filename) as f:
            ast = self._parser.parse(f.read())
        return ast

    def parse_string(self, text):
        """
        Load code from a textfile and return a parse tree.

        Parameter:
            filename : [text] source

        Return:
            [lark.tree] parse tree
        """
        ast = self._parser.parse(text)
        return ast

    @property
    def parser(self):
        return self.parser

    @parser.setter
    def parser(self, new_parser):
        assert isinstance(new_parser, Lark), "Only Lark objects supported"
        self._parser = new_parser

    @staticmethod
    def get_grammar(file_or_folder):
        grammar = ""
        for filename in to_filename_tuple(
            file_or_folder, extensions=(".g", ".grammar", ".lark")
        ):
            with open(filename) as f:
                grammar += f.read()
        return grammar
