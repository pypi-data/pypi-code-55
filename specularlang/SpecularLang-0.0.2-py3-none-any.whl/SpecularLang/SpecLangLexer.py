# Generated from C:/Users/Emery/PycharmProjects/SpecularLang\SpecLang.g4 by ANTLR 4.8
from antlr4 import *
from io import StringIO
from typing.io import TextIO
import sys


from antlr_denter.DenterHelper import DenterHelper
from SpecularLang.SpecLangParser import SpecLangParser



def serializedATN():
    with StringIO() as buf:
        buf.write("\3\u608b\ua72a\u8133\ub9ed\u417c\u3be7\u7786\u5964\2+")
        buf.write("\u0110\b\1\4\2\t\2\4\3\t\3\4\4\t\4\4\5\t\5\4\6\t\6\4\7")
        buf.write("\t\7\4\b\t\b\4\t\t\t\4\n\t\n\4\13\t\13\4\f\t\f\4\r\t\r")
        buf.write("\4\16\t\16\4\17\t\17\4\20\t\20\4\21\t\21\4\22\t\22\4\23")
        buf.write("\t\23\4\24\t\24\4\25\t\25\4\26\t\26\4\27\t\27\4\30\t\30")
        buf.write("\4\31\t\31\4\32\t\32\4\33\t\33\4\34\t\34\4\35\t\35\4\36")
        buf.write("\t\36\4\37\t\37\4 \t \4!\t!\4\"\t\"\4#\t#\4$\t$\4%\t%")
        buf.write("\4&\t&\4\'\t\'\4(\t(\4)\t)\4*\t*\3\2\3\2\3\3\3\3\3\4\3")
        buf.write("\4\3\4\3\4\3\4\3\4\3\4\3\5\3\5\3\6\3\6\3\7\3\7\3\b\3\b")
        buf.write("\3\t\3\t\3\n\3\n\3\13\3\13\3\13\3\f\3\f\3\f\3\r\3\r\3")
        buf.write("\16\3\16\3\16\3\17\3\17\3\17\3\17\3\17\3\17\3\20\3\20")
        buf.write("\3\20\3\20\3\20\3\20\3\21\3\21\3\21\3\21\3\21\3\21\3\22")
        buf.write("\3\22\3\22\3\22\3\22\3\23\3\23\3\23\3\24\3\24\3\24\3\25")
        buf.write("\3\25\3\25\3\26\3\26\3\26\3\26\3\26\3\27\3\27\3\27\3\27")
        buf.write("\3\27\3\30\3\30\3\30\3\30\3\30\3\30\3\31\3\31\3\31\3\31")
        buf.write("\3\31\3\31\3\31\3\32\3\32\3\32\3\32\3\33\3\33\3\33\3\34")
        buf.write("\3\34\3\34\3\34\3\35\3\35\3\36\3\36\3\37\3\37\3 \3 \3")
        buf.write("!\3!\3!\3!\7!\u00c6\n!\f!\16!\u00c9\13!\3!\3!\3\"\3\"")
        buf.write("\3\"\3\"\3\"\3#\3#\3#\3#\3#\3#\3$\3$\3$\3$\3$\3%\3%\3")
        buf.write("%\3%\3%\3%\3%\3&\3&\3&\3&\3&\3&\3&\3&\3\'\3\'\7\'\u00ee")
        buf.write("\n\'\f\'\16\'\u00f1\13\'\3(\6(\u00f4\n(\r(\16(\u00f5\3")
        buf.write(")\5)\u00f9\n)\3)\3)\7)\u00fd\n)\f)\16)\u0100\13)\3)\7")
        buf.write(")\u0103\n)\f)\16)\u0106\13)\5)\u0108\n)\3*\6*\u010b\n")
        buf.write("*\r*\16*\u010c\3*\3*\4\u00c7\u010c\2+\3\3\5\4\7\5\t\6")
        buf.write("\13\7\r\b\17\t\21\n\23\13\25\f\27\r\31\16\33\17\35\20")
        buf.write("\37\21!\22#\23%\24\'\25)\26+\27-\30/\31\61\32\63\33\65")
        buf.write("\34\67\359\36;\37= ?!A\"C#E$G%I&K\'M(O)Q*S+\3\2\6\5\2")
        buf.write("C\\aac|\6\2\62;C\\aac|\3\2\62;\3\2\"\"\2\u0118\2\3\3\2")
        buf.write("\2\2\2\5\3\2\2\2\2\7\3\2\2\2\2\t\3\2\2\2\2\13\3\2\2\2")
        buf.write("\2\r\3\2\2\2\2\17\3\2\2\2\2\21\3\2\2\2\2\23\3\2\2\2\2")
        buf.write("\25\3\2\2\2\2\27\3\2\2\2\2\31\3\2\2\2\2\33\3\2\2\2\2\35")
        buf.write("\3\2\2\2\2\37\3\2\2\2\2!\3\2\2\2\2#\3\2\2\2\2%\3\2\2\2")
        buf.write("\2\'\3\2\2\2\2)\3\2\2\2\2+\3\2\2\2\2-\3\2\2\2\2/\3\2\2")
        buf.write("\2\2\61\3\2\2\2\2\63\3\2\2\2\2\65\3\2\2\2\2\67\3\2\2\2")
        buf.write("\29\3\2\2\2\2;\3\2\2\2\2=\3\2\2\2\2?\3\2\2\2\2A\3\2\2")
        buf.write("\2\2C\3\2\2\2\2E\3\2\2\2\2G\3\2\2\2\2I\3\2\2\2\2K\3\2")
        buf.write("\2\2\2M\3\2\2\2\2O\3\2\2\2\2Q\3\2\2\2\2S\3\2\2\2\3U\3")
        buf.write("\2\2\2\5W\3\2\2\2\7Y\3\2\2\2\t`\3\2\2\2\13b\3\2\2\2\r")
        buf.write("d\3\2\2\2\17f\3\2\2\2\21h\3\2\2\2\23j\3\2\2\2\25l\3\2")
        buf.write("\2\2\27o\3\2\2\2\31r\3\2\2\2\33t\3\2\2\2\35w\3\2\2\2\37")
        buf.write("}\3\2\2\2!\u0083\3\2\2\2#\u0089\3\2\2\2%\u008e\3\2\2\2")
        buf.write("\'\u0091\3\2\2\2)\u0094\3\2\2\2+\u0097\3\2\2\2-\u009c")
        buf.write("\3\2\2\2/\u00a1\3\2\2\2\61\u00a7\3\2\2\2\63\u00ae\3\2")
        buf.write("\2\2\65\u00b2\3\2\2\2\67\u00b5\3\2\2\29\u00b9\3\2\2\2")
        buf.write(";\u00bb\3\2\2\2=\u00bd\3\2\2\2?\u00bf\3\2\2\2A\u00c1\3")
        buf.write("\2\2\2C\u00cc\3\2\2\2E\u00d1\3\2\2\2G\u00d7\3\2\2\2I\u00dc")
        buf.write("\3\2\2\2K\u00e3\3\2\2\2M\u00eb\3\2\2\2O\u00f3\3\2\2\2")
        buf.write("Q\u00f8\3\2\2\2S\u010a\3\2\2\2UV\7]\2\2V\4\3\2\2\2WX\7")
        buf.write("_\2\2X\6\3\2\2\2YZ\7e\2\2Z[\7w\2\2[\\\7u\2\2\\]\7v\2\2")
        buf.write("]^\7q\2\2^_\7o\2\2_\b\3\2\2\2`a\7<\2\2a\n\3\2\2\2bc\7")
        buf.write("?\2\2c\f\3\2\2\2de\7B\2\2e\16\3\2\2\2fg\7*\2\2g\20\3\2")
        buf.write("\2\2hi\7+\2\2i\22\3\2\2\2jk\7=\2\2k\24\3\2\2\2lm\7?\2")
        buf.write("\2mn\7?\2\2n\26\3\2\2\2op\7#\2\2pq\7?\2\2q\30\3\2\2\2")
        buf.write("rs\7.\2\2s\32\3\2\2\2tu\7/\2\2uv\7@\2\2v\34\3\2\2\2wx")
        buf.write("\7y\2\2xy\7j\2\2yz\7k\2\2z{\7n\2\2{|\7g\2\2|\36\3\2\2")
        buf.write("\2}~\7g\2\2~\177\7p\2\2\177\u0080\7v\2\2\u0080\u0081\7")
        buf.write("g\2\2\u0081\u0082\7t\2\2\u0082 \3\2\2\2\u0083\u0084\7")
        buf.write("g\2\2\u0084\u0085\7z\2\2\u0085\u0086\7k\2\2\u0086\u0087")
        buf.write("\7v\2\2\u0087\u0088\7u\2\2\u0088\"\3\2\2\2\u0089\u008a")
        buf.write("\7o\2\2\u008a\u008b\7q\2\2\u008b\u008c\7x\2\2\u008c\u008d")
        buf.write("\7g\2\2\u008d$\3\2\2\2\u008e\u008f\7v\2\2\u008f\u0090")
        buf.write("\7q\2\2\u0090&\3\2\2\2\u0091\u0092\7f\2\2\u0092\u0093")
        buf.write("\7q\2\2\u0093(\3\2\2\2\u0094\u0095\7k\2\2\u0095\u0096")
        buf.write("\7h\2\2\u0096*\3\2\2\2\u0097\u0098\7g\2\2\u0098\u0099")
        buf.write("\7n\2\2\u0099\u009a\7k\2\2\u009a\u009b\7h\2\2\u009b,\3")
        buf.write("\2\2\2\u009c\u009d\7g\2\2\u009d\u009e\7n\2\2\u009e\u009f")
        buf.write("\7u\2\2\u009f\u00a0\7g\2\2\u00a0.\3\2\2\2\u00a1\u00a2")
        buf.write("\7u\2\2\u00a2\u00a3\7e\2\2\u00a3\u00a4\7g\2\2\u00a4\u00a5")
        buf.write("\7p\2\2\u00a5\u00a6\7g\2\2\u00a6\60\3\2\2\2\u00a7\u00a8")
        buf.write("\7i\2\2\u00a8\u00a9\7n\2\2\u00a9\u00aa\7q\2\2\u00aa\u00ab")
        buf.write("\7d\2\2\u00ab\u00ac\7c\2\2\u00ac\u00ad\7n\2\2\u00ad\62")
        buf.write("\3\2\2\2\u00ae\u00af\7c\2\2\u00af\u00b0\7p\2\2\u00b0\u00b1")
        buf.write("\7f\2\2\u00b1\64\3\2\2\2\u00b2\u00b3\7q\2\2\u00b3\u00b4")
        buf.write("\7t\2\2\u00b4\66\3\2\2\2\u00b5\u00b6\7p\2\2\u00b6\u00b7")
        buf.write("\7q\2\2\u00b7\u00b8\7v\2\2\u00b88\3\2\2\2\u00b9\u00ba")
        buf.write("\7,\2\2\u00ba:\3\2\2\2\u00bb\u00bc\7\61\2\2\u00bc<\3\2")
        buf.write("\2\2\u00bd\u00be\7-\2\2\u00be>\3\2\2\2\u00bf\u00c0\7/")
        buf.write("\2\2\u00c0@\3\2\2\2\u00c1\u00c7\7$\2\2\u00c2\u00c3\7^")
        buf.write("\2\2\u00c3\u00c6\7$\2\2\u00c4\u00c6\13\2\2\2\u00c5\u00c2")
        buf.write("\3\2\2\2\u00c5\u00c4\3\2\2\2\u00c6\u00c9\3\2\2\2\u00c7")
        buf.write("\u00c8\3\2\2\2\u00c7\u00c5\3\2\2\2\u00c8\u00ca\3\2\2\2")
        buf.write("\u00c9\u00c7\3\2\2\2\u00ca\u00cb\7$\2\2\u00cbB\3\2\2\2")
        buf.write("\u00cc\u00cd\7V\2\2\u00cd\u00ce\7t\2\2\u00ce\u00cf\7w")
        buf.write("\2\2\u00cf\u00d0\7g\2\2\u00d0D\3\2\2\2\u00d1\u00d2\7H")
        buf.write("\2\2\u00d2\u00d3\7c\2\2\u00d3\u00d4\7n\2\2\u00d4\u00d5")
        buf.write("\7u\2\2\u00d5\u00d6\7g\2\2\u00d6F\3\2\2\2\u00d7\u00d8")
        buf.write("\7P\2\2\u00d8\u00d9\7q\2\2\u00d9\u00da\7p\2\2\u00da\u00db")
        buf.write("\7g\2\2\u00dbH\3\2\2\2\u00dc\u00dd\7h\2\2\u00dd\u00de")
        buf.write("\7c\2\2\u00de\u00df\7f\2\2\u00df\u00e0\7g\2\2\u00e0\u00e1")
        buf.write("\7k\2\2\u00e1\u00e2\7p\2\2\u00e2J\3\2\2\2\u00e3\u00e4")
        buf.write("\7h\2\2\u00e4\u00e5\7c\2\2\u00e5\u00e6\7f\2\2\u00e6\u00e7")
        buf.write("\7g\2\2\u00e7\u00e8\7q\2\2\u00e8\u00e9\7w\2\2\u00e9\u00ea")
        buf.write("\7v\2\2\u00eaL\3\2\2\2\u00eb\u00ef\t\2\2\2\u00ec\u00ee")
        buf.write("\t\3\2\2\u00ed\u00ec\3\2\2\2\u00ee\u00f1\3\2\2\2\u00ef")
        buf.write("\u00ed\3\2\2\2\u00ef\u00f0\3\2\2\2\u00f0N\3\2\2\2\u00f1")
        buf.write("\u00ef\3\2\2\2\u00f2\u00f4\t\4\2\2\u00f3\u00f2\3\2\2\2")
        buf.write("\u00f4\u00f5\3\2\2\2\u00f5\u00f3\3\2\2\2\u00f5\u00f6\3")
        buf.write("\2\2\2\u00f6P\3\2\2\2\u00f7\u00f9\7\17\2\2\u00f8\u00f7")
        buf.write("\3\2\2\2\u00f8\u00f9\3\2\2\2\u00f9\u00fa\3\2\2\2\u00fa")
        buf.write("\u0107\7\f\2\2\u00fb\u00fd\7\13\2\2\u00fc\u00fb\3\2\2")
        buf.write("\2\u00fd\u0100\3\2\2\2\u00fe\u00fc\3\2\2\2\u00fe\u00ff")
        buf.write("\3\2\2\2\u00ff\u0108\3\2\2\2\u0100\u00fe\3\2\2\2\u0101")
        buf.write("\u0103\7\"\2\2\u0102\u0101\3\2\2\2\u0103\u0106\3\2\2\2")
        buf.write("\u0104\u0102\3\2\2\2\u0104\u0105\3\2\2\2\u0105\u0108\3")
        buf.write("\2\2\2\u0106\u0104\3\2\2\2\u0107\u00fe\3\2\2\2\u0107\u0104")
        buf.write("\3\2\2\2\u0108R\3\2\2\2\u0109\u010b\t\5\2\2\u010a\u0109")
        buf.write("\3\2\2\2\u010b\u010c\3\2\2\2\u010c\u010d\3\2\2\2\u010c")
        buf.write("\u010a\3\2\2\2\u010d\u010e\3\2\2\2\u010e\u010f\b*\2\2")
        buf.write("\u010fT\3\2\2\2\f\2\u00c5\u00c7\u00ef\u00f5\u00f8\u00fe")
        buf.write("\u0104\u0107\u010c\3\b\2\2")
        return buf.getvalue()


class SpecLangLexer(Lexer):

    atn = ATNDeserializer().deserialize(serializedATN())

    decisionsToDFA = [ DFA(ds, i) for i, ds in enumerate(atn.decisionToState) ]

    T__0 = 1
    T__1 = 2
    T__2 = 3
    T__3 = 4
    T__4 = 5
    T__5 = 6
    T__6 = 7
    T__7 = 8
    T__8 = 9
    T__9 = 10
    T__10 = 11
    T__11 = 12
    NEXT = 13
    WHILE = 14
    ENTER = 15
    EXITS = 16
    MOVE = 17
    TO = 18
    DO = 19
    IF = 20
    ELIF = 21
    ELSE = 22
    SCENE = 23
    GLOBAL = 24
    AND = 25
    OR = 26
    NOT = 27
    MUL = 28
    DIV = 29
    ADD = 30
    SUB = 31
    STRING = 32
    TRUE = 33
    FALSE = 34
    NONE = 35
    FADEIN = 36
    FADEOUT = 37
    ID = 38
    NUMBER = 39
    NEWLINE = 40
    WS = 41

    channelNames = [ u"DEFAULT_TOKEN_CHANNEL", u"HIDDEN" ]

    modeNames = [ "DEFAULT_MODE" ]

    literalNames = [ "<INVALID>",
            "'['", "']'", "'custom'", "':'", "'='", "'@'", "'('", "')'", 
            "';'", "'=='", "'!='", "','", "'->'", "'while'", "'enter'", 
            "'exits'", "'move'", "'to'", "'do'", "'if'", "'elif'", "'else'", 
            "'scene'", "'global'", "'and'", "'or'", "'not'", "'*'", "'/'", 
            "'+'", "'-'", "'True'", "'False'", "'None'", "'fadein'", "'fadeout'" ]

    symbolicNames = [ "<INVALID>",
            "NEXT", "WHILE", "ENTER", "EXITS", "MOVE", "TO", "DO", "IF", 
            "ELIF", "ELSE", "SCENE", "GLOBAL", "AND", "OR", "NOT", "MUL", 
            "DIV", "ADD", "SUB", "STRING", "TRUE", "FALSE", "NONE", "FADEIN", 
            "FADEOUT", "ID", "NUMBER", "NEWLINE", "WS" ]

    ruleNames = [ "T__0", "T__1", "T__2", "T__3", "T__4", "T__5", "T__6", 
                  "T__7", "T__8", "T__9", "T__10", "T__11", "NEXT", "WHILE", 
                  "ENTER", "EXITS", "MOVE", "TO", "DO", "IF", "ELIF", "ELSE", 
                  "SCENE", "GLOBAL", "AND", "OR", "NOT", "MUL", "DIV", "ADD", 
                  "SUB", "STRING", "TRUE", "FALSE", "NONE", "FADEIN", "FADEOUT", 
                  "ID", "NUMBER", "NEWLINE", "WS" ]

    grammarFileName = "SpecLang.g4"

    def __init__(self, input=None, output:TextIO = sys.stdout):
        super().__init__(input, output)
        self.checkVersion("4.8")
        self._interp = LexerATNSimulator(self, self.atn, self.decisionsToDFA, PredictionContextCache())
        self._actions = None
        self._predicates = None


    class SpecDenter(DenterHelper):
        def __init__(self, lexer, nl_token, indent_token, dedent_token, ignore_eof):
            super().__init__(nl_token, indent_token, dedent_token, ignore_eof)
            self.lexer: SpecLangLexer = lexer

        def pull_token(self):
            return super(SpecLangLexer, self.lexer).nextToken()

    denter = None

    def nextToken(self):
        if not self.denter:
            self.denter = self.SpecDenter(self, self.NEWLINE, SpecLangParser.INDENT, SpecLangParser.DEDENT, False)
        return self.denter.next_token()



