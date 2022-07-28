# Generated from .\Mascheroni.g4 by ANTLR 4.9.3
from antlr4 import *
if __name__ is not None and "." in __name__:
    from .MascheroniParser import MascheroniParser
else:
    from MascheroniParser import MascheroniParser

# This class defines a complete generic visitor for a parse tree produced by MascheroniParser.

class MascheroniVisitor(ParseTreeVisitor):

    # Visit a parse tree produced by MascheroniParser#start.
    def visitStart(self, ctx:MascheroniParser.StartContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MascheroniParser#BaseConstruct.
    def visitBaseConstruct(self, ctx:MascheroniParser.BaseConstructContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MascheroniParser#InductiveConstruct.
    def visitInductiveConstruct(self, ctx:MascheroniParser.InductiveConstructContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MascheroniParser#base_construct_res.
    def visitBase_construct_res(self, ctx:MascheroniParser.Base_construct_resContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MascheroniParser#base_construct_params.
    def visitBase_construct_params(self, ctx:MascheroniParser.Base_construct_paramsContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MascheroniParser#inductive_construct_res.
    def visitInductive_construct_res(self, ctx:MascheroniParser.Inductive_construct_resContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MascheroniParser#inductive_construct_params.
    def visitInductive_construct_params(self, ctx:MascheroniParser.Inductive_construct_paramsContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MascheroniParser#StepShow.
    def visitStepShow(self, ctx:MascheroniParser.StepShowContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MascheroniParser#StepAssignement.
    def visitStepAssignement(self, ctx:MascheroniParser.StepAssignementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MascheroniParser#StepDefine.
    def visitStepDefine(self, ctx:MascheroniParser.StepDefineContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MascheroniParser#StepWith.
    def visitStepWith(self, ctx:MascheroniParser.StepWithContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MascheroniParser#StepIfs.
    def visitStepIfs(self, ctx:MascheroniParser.StepIfsContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MascheroniParser#ShowNoLabel.
    def visitShowNoLabel(self, ctx:MascheroniParser.ShowNoLabelContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MascheroniParser#ShowLabel.
    def visitShowLabel(self, ctx:MascheroniParser.ShowLabelContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MascheroniParser#IfThen.
    def visitIfThen(self, ctx:MascheroniParser.IfThenContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MascheroniParser#IfElseThen.
    def visitIfElseThen(self, ctx:MascheroniParser.IfElseThenContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MascheroniParser#ConditionNot.
    def visitConditionNot(self, ctx:MascheroniParser.ConditionNotContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MascheroniParser#ConditionComparison.
    def visitConditionComparison(self, ctx:MascheroniParser.ConditionComparisonContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MascheroniParser#ConditionEquality.
    def visitConditionEquality(self, ctx:MascheroniParser.ConditionEqualityContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MascheroniParser#ConditionParens.
    def visitConditionParens(self, ctx:MascheroniParser.ConditionParensContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MascheroniParser#named_expression.
    def visitNamed_expression(self, ctx:MascheroniParser.Named_expressionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MascheroniParser#InductiveExpression.
    def visitInductiveExpression(self, ctx:MascheroniParser.InductiveExpressionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MascheroniParser#InductiveNameName.
    def visitInductiveNameName(self, ctx:MascheroniParser.InductiveNameNameContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MascheroniParser#InductiveInt.
    def visitInductiveInt(self, ctx:MascheroniParser.InductiveIntContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MascheroniParser#InductiveName.
    def visitInductiveName(self, ctx:MascheroniParser.InductiveNameContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MascheroniParser#inductive_names.
    def visitInductive_names(self, ctx:MascheroniParser.Inductive_namesContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MascheroniParser#EnteExpressionIntersection.
    def visitEnteExpressionIntersection(self, ctx:MascheroniParser.EnteExpressionIntersectionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MascheroniParser#EnteExpressionName.
    def visitEnteExpressionName(self, ctx:MascheroniParser.EnteExpressionNameContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MascheroniParser#EnteExpressionPrimitive.
    def visitEnteExpressionPrimitive(self, ctx:MascheroniParser.EnteExpressionPrimitiveContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MascheroniParser#EnteExpressionInvocation.
    def visitEnteExpressionInvocation(self, ctx:MascheroniParser.EnteExpressionInvocationContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MascheroniParser#invocation_params.
    def visitInvocation_params(self, ctx:MascheroniParser.Invocation_paramsContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MascheroniParser#IntExpressionAddSub.
    def visitIntExpressionAddSub(self, ctx:MascheroniParser.IntExpressionAddSubContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MascheroniParser#IntExpressionID.
    def visitIntExpressionID(self, ctx:MascheroniParser.IntExpressionIDContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MascheroniParser#IntExpressionParens.
    def visitIntExpressionParens(self, ctx:MascheroniParser.IntExpressionParensContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MascheroniParser#IntExpressionMulDivMod.
    def visitIntExpressionMulDivMod(self, ctx:MascheroniParser.IntExpressionMulDivModContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MascheroniParser#IntExpressionInt.
    def visitIntExpressionInt(self, ctx:MascheroniParser.IntExpressionIntContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MascheroniParser#int_name.
    def visitInt_name(self, ctx:MascheroniParser.Int_nameContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MascheroniParser#name_name.
    def visitName_name(self, ctx:MascheroniParser.Name_nameContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MascheroniParser#expression_name.
    def visitExpression_name(self, ctx:MascheroniParser.Expression_nameContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MascheroniParser#typed_name.
    def visitTyped_name(self, ctx:MascheroniParser.Typed_nameContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MascheroniParser#typed_int_name.
    def visitTyped_int_name(self, ctx:MascheroniParser.Typed_int_nameContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MascheroniParser#typed_name_name.
    def visitTyped_name_name(self, ctx:MascheroniParser.Typed_name_nameContext):
        return self.visitChildren(ctx)



del MascheroniParser