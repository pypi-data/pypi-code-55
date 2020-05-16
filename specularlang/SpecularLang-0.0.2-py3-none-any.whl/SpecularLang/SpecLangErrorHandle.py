from antlr4 import RecognitionException
from antlr4.error.ErrorListener import ErrorListener
from antlr4.error.ErrorStrategy import DefaultErrorStrategy
from antlr4.error.Errors import InputMismatchException

from SpecularLang.SpecLangLexer import SpecLangLexer


class SpecLangParserErrorStrategy(DefaultErrorStrategy):

    def recover(self, recognizer, e: RecognitionException):
        raise RuntimeError(e)

    def recoverInline(self, recognizer):
        raise RuntimeError(InputMismatchException(recognizer))

    def sync(self, recognizer):
        pass


class BailSimpleLexer(SpecLangLexer):
    def __init__(self, input):
        super().__init__(input)

    def recover(self, re:RecognitionException):
        raise RuntimeError(re)


class SpecLangErrorListener(ErrorListener):
    def syntaxError(self, recognizer, offendingSymbol, line, column, msg, e):
        stack = recognizer.getRuleInvocationStack()
        stack.reverse()
        print("rule stack: ", str(stack))
        print("line", line, ":", column, "at", offendingSymbol, ":", msg)