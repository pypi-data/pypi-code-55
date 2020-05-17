# Generated from C:/Users/Emery/PycharmProjects/SpecularLang\SpecLang.g4 by ANTLR 4.8
from antlr4 import *
if __name__ is not None and "." in __name__:
    from .SpecLangParser import SpecLangParser
else:
    from SpecularLang.SpecLangParser import SpecLangParser

# This class defines a complete generic visitor for a parse tree produced by SpecLangParser.

class SpecLangVisitor(ParseTreeVisitor):

    # Visit a parse tree produced by SpecLangParser#program.
    def visitProgram(self, ctx:SpecLangParser.ProgramContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SpecLangParser#block.
    def visitBlock(self, ctx:SpecLangParser.BlockContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SpecLangParser#simple_statement.
    def visitSimple_statement(self, ctx:SpecLangParser.Simple_statementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SpecLangParser#enter.
    def visitEnter(self, ctx:SpecLangParser.EnterContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SpecLangParser#exit.
    def visitExit(self, ctx:SpecLangParser.ExitContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SpecLangParser#move.
    def visitMove(self, ctx:SpecLangParser.MoveContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SpecLangParser#fadeIn.
    def visitFadeIn(self, ctx:SpecLangParser.FadeInContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SpecLangParser#fadeOut.
    def visitFadeOut(self, ctx:SpecLangParser.FadeOutContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SpecLangParser#customDirection.
    def visitCustomDirection(self, ctx:SpecLangParser.CustomDirectionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SpecLangParser#assignment.
    def visitAssignment(self, ctx:SpecLangParser.AssignmentContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SpecLangParser#dialog.
    def visitDialog(self, ctx:SpecLangParser.DialogContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SpecLangParser#emotion.
    def visitEmotion(self, ctx:SpecLangParser.EmotionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SpecLangParser#complex_statement.
    def visitComplex_statement(self, ctx:SpecLangParser.Complex_statementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SpecLangParser#ifstatement.
    def visitIfstatement(self, ctx:SpecLangParser.IfstatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SpecLangParser#else_if_statement.
    def visitElse_if_statement(self, ctx:SpecLangParser.Else_if_statementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SpecLangParser#else_statement.
    def visitElse_statement(self, ctx:SpecLangParser.Else_statementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SpecLangParser#whileLoop.
    def visitWhileLoop(self, ctx:SpecLangParser.WhileLoopContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SpecLangParser#scene_statement.
    def visitScene_statement(self, ctx:SpecLangParser.Scene_statementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SpecLangParser#add.
    def visitAdd(self, ctx:SpecLangParser.AddContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SpecLangParser#equal.
    def visitEqual(self, ctx:SpecLangParser.EqualContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SpecLangParser#paren.
    def visitParen(self, ctx:SpecLangParser.ParenContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SpecLangParser#mult.
    def visitMult(self, ctx:SpecLangParser.MultContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SpecLangParser#or.
    def visitOr(self, ctx:SpecLangParser.OrContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SpecLangParser#and.
    def visitAnd(self, ctx:SpecLangParser.AndContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SpecLangParser#term.
    def visitTerm(self, ctx:SpecLangParser.TermContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SpecLangParser#unary.
    def visitUnary(self, ctx:SpecLangParser.UnaryContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SpecLangParser#choice.
    def visitChoice(self, ctx:SpecLangParser.ChoiceContext):
        return self.visitChildren(ctx)



del SpecLangParser