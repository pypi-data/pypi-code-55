# Generated from C:/Users/Emery/PycharmProjects/SpecularLang\SpecLang.g4 by ANTLR 4.8
from antlr4 import *
if __name__ is not None and "." in __name__:
    from .SpecLangParser import SpecLangParser
else:
    from SpecularLang.SpecLangParser import SpecLangParser

# This class defines a complete listener for a parse tree produced by SpecLangParser.
class SpecLangListener(ParseTreeListener):

    # Enter a parse tree produced by SpecLangParser#program.
    def enterProgram(self, ctx:SpecLangParser.ProgramContext):
        pass

    # Exit a parse tree produced by SpecLangParser#program.
    def exitProgram(self, ctx:SpecLangParser.ProgramContext):
        pass


    # Enter a parse tree produced by SpecLangParser#block.
    def enterBlock(self, ctx:SpecLangParser.BlockContext):
        pass

    # Exit a parse tree produced by SpecLangParser#block.
    def exitBlock(self, ctx:SpecLangParser.BlockContext):
        pass


    # Enter a parse tree produced by SpecLangParser#simple_statement.
    def enterSimple_statement(self, ctx:SpecLangParser.Simple_statementContext):
        pass

    # Exit a parse tree produced by SpecLangParser#simple_statement.
    def exitSimple_statement(self, ctx:SpecLangParser.Simple_statementContext):
        pass


    # Enter a parse tree produced by SpecLangParser#enter.
    def enterEnter(self, ctx:SpecLangParser.EnterContext):
        pass

    # Exit a parse tree produced by SpecLangParser#enter.
    def exitEnter(self, ctx:SpecLangParser.EnterContext):
        pass


    # Enter a parse tree produced by SpecLangParser#exit.
    def enterExit(self, ctx:SpecLangParser.ExitContext):
        pass

    # Exit a parse tree produced by SpecLangParser#exit.
    def exitExit(self, ctx:SpecLangParser.ExitContext):
        pass


    # Enter a parse tree produced by SpecLangParser#move.
    def enterMove(self, ctx:SpecLangParser.MoveContext):
        pass

    # Exit a parse tree produced by SpecLangParser#move.
    def exitMove(self, ctx:SpecLangParser.MoveContext):
        pass


    # Enter a parse tree produced by SpecLangParser#fadeIn.
    def enterFadeIn(self, ctx:SpecLangParser.FadeInContext):
        pass

    # Exit a parse tree produced by SpecLangParser#fadeIn.
    def exitFadeIn(self, ctx:SpecLangParser.FadeInContext):
        pass


    # Enter a parse tree produced by SpecLangParser#fadeOut.
    def enterFadeOut(self, ctx:SpecLangParser.FadeOutContext):
        pass

    # Exit a parse tree produced by SpecLangParser#fadeOut.
    def exitFadeOut(self, ctx:SpecLangParser.FadeOutContext):
        pass


    # Enter a parse tree produced by SpecLangParser#customDirection.
    def enterCustomDirection(self, ctx:SpecLangParser.CustomDirectionContext):
        pass

    # Exit a parse tree produced by SpecLangParser#customDirection.
    def exitCustomDirection(self, ctx:SpecLangParser.CustomDirectionContext):
        pass


    # Enter a parse tree produced by SpecLangParser#assignment.
    def enterAssignment(self, ctx:SpecLangParser.AssignmentContext):
        pass

    # Exit a parse tree produced by SpecLangParser#assignment.
    def exitAssignment(self, ctx:SpecLangParser.AssignmentContext):
        pass


    # Enter a parse tree produced by SpecLangParser#dialog.
    def enterDialog(self, ctx:SpecLangParser.DialogContext):
        pass

    # Exit a parse tree produced by SpecLangParser#dialog.
    def exitDialog(self, ctx:SpecLangParser.DialogContext):
        pass


    # Enter a parse tree produced by SpecLangParser#emotion.
    def enterEmotion(self, ctx:SpecLangParser.EmotionContext):
        pass

    # Exit a parse tree produced by SpecLangParser#emotion.
    def exitEmotion(self, ctx:SpecLangParser.EmotionContext):
        pass


    # Enter a parse tree produced by SpecLangParser#complex_statement.
    def enterComplex_statement(self, ctx:SpecLangParser.Complex_statementContext):
        pass

    # Exit a parse tree produced by SpecLangParser#complex_statement.
    def exitComplex_statement(self, ctx:SpecLangParser.Complex_statementContext):
        pass


    # Enter a parse tree produced by SpecLangParser#ifstatement.
    def enterIfstatement(self, ctx:SpecLangParser.IfstatementContext):
        pass

    # Exit a parse tree produced by SpecLangParser#ifstatement.
    def exitIfstatement(self, ctx:SpecLangParser.IfstatementContext):
        pass


    # Enter a parse tree produced by SpecLangParser#else_if_statement.
    def enterElse_if_statement(self, ctx:SpecLangParser.Else_if_statementContext):
        pass

    # Exit a parse tree produced by SpecLangParser#else_if_statement.
    def exitElse_if_statement(self, ctx:SpecLangParser.Else_if_statementContext):
        pass


    # Enter a parse tree produced by SpecLangParser#else_statement.
    def enterElse_statement(self, ctx:SpecLangParser.Else_statementContext):
        pass

    # Exit a parse tree produced by SpecLangParser#else_statement.
    def exitElse_statement(self, ctx:SpecLangParser.Else_statementContext):
        pass


    # Enter a parse tree produced by SpecLangParser#whileLoop.
    def enterWhileLoop(self, ctx:SpecLangParser.WhileLoopContext):
        pass

    # Exit a parse tree produced by SpecLangParser#whileLoop.
    def exitWhileLoop(self, ctx:SpecLangParser.WhileLoopContext):
        pass


    # Enter a parse tree produced by SpecLangParser#scene_statement.
    def enterScene_statement(self, ctx:SpecLangParser.Scene_statementContext):
        pass

    # Exit a parse tree produced by SpecLangParser#scene_statement.
    def exitScene_statement(self, ctx:SpecLangParser.Scene_statementContext):
        pass


    # Enter a parse tree produced by SpecLangParser#add.
    def enterAdd(self, ctx:SpecLangParser.AddContext):
        pass

    # Exit a parse tree produced by SpecLangParser#add.
    def exitAdd(self, ctx:SpecLangParser.AddContext):
        pass


    # Enter a parse tree produced by SpecLangParser#equal.
    def enterEqual(self, ctx:SpecLangParser.EqualContext):
        pass

    # Exit a parse tree produced by SpecLangParser#equal.
    def exitEqual(self, ctx:SpecLangParser.EqualContext):
        pass


    # Enter a parse tree produced by SpecLangParser#paren.
    def enterParen(self, ctx:SpecLangParser.ParenContext):
        pass

    # Exit a parse tree produced by SpecLangParser#paren.
    def exitParen(self, ctx:SpecLangParser.ParenContext):
        pass


    # Enter a parse tree produced by SpecLangParser#mult.
    def enterMult(self, ctx:SpecLangParser.MultContext):
        pass

    # Exit a parse tree produced by SpecLangParser#mult.
    def exitMult(self, ctx:SpecLangParser.MultContext):
        pass


    # Enter a parse tree produced by SpecLangParser#or.
    def enterOr(self, ctx:SpecLangParser.OrContext):
        pass

    # Exit a parse tree produced by SpecLangParser#or.
    def exitOr(self, ctx:SpecLangParser.OrContext):
        pass


    # Enter a parse tree produced by SpecLangParser#and.
    def enterAnd(self, ctx:SpecLangParser.AndContext):
        pass

    # Exit a parse tree produced by SpecLangParser#and.
    def exitAnd(self, ctx:SpecLangParser.AndContext):
        pass


    # Enter a parse tree produced by SpecLangParser#term.
    def enterTerm(self, ctx:SpecLangParser.TermContext):
        pass

    # Exit a parse tree produced by SpecLangParser#term.
    def exitTerm(self, ctx:SpecLangParser.TermContext):
        pass


    # Enter a parse tree produced by SpecLangParser#unary.
    def enterUnary(self, ctx:SpecLangParser.UnaryContext):
        pass

    # Exit a parse tree produced by SpecLangParser#unary.
    def exitUnary(self, ctx:SpecLangParser.UnaryContext):
        pass


    # Enter a parse tree produced by SpecLangParser#choice.
    def enterChoice(self, ctx:SpecLangParser.ChoiceContext):
        pass

    # Exit a parse tree produced by SpecLangParser#choice.
    def exitChoice(self, ctx:SpecLangParser.ChoiceContext):
        pass



del SpecLangParser