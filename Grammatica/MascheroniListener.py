# Generated from .\Mascheroni.g4 by ANTLR 4.9.3
from antlr4 import *
if __name__ is not None and "." in __name__:
    from .MascheroniParser import MascheroniParser
else:
    from MascheroniParser import MascheroniParser

# This class defines a complete listener for a parse tree produced by MascheroniParser.
class MascheroniListener(ParseTreeListener):

    # Enter a parse tree produced by MascheroniParser#start.
    def enterStart(self, ctx:MascheroniParser.StartContext):
        pass

    # Exit a parse tree produced by MascheroniParser#start.
    def exitStart(self, ctx:MascheroniParser.StartContext):
        pass


    # Enter a parse tree produced by MascheroniParser#BaseConstruct.
    def enterBaseConstruct(self, ctx:MascheroniParser.BaseConstructContext):
        pass

    # Exit a parse tree produced by MascheroniParser#BaseConstruct.
    def exitBaseConstruct(self, ctx:MascheroniParser.BaseConstructContext):
        pass


    # Enter a parse tree produced by MascheroniParser#InductiveConstruct.
    def enterInductiveConstruct(self, ctx:MascheroniParser.InductiveConstructContext):
        pass

    # Exit a parse tree produced by MascheroniParser#InductiveConstruct.
    def exitInductiveConstruct(self, ctx:MascheroniParser.InductiveConstructContext):
        pass


    # Enter a parse tree produced by MascheroniParser#base_construct_res.
    def enterBase_construct_res(self, ctx:MascheroniParser.Base_construct_resContext):
        pass

    # Exit a parse tree produced by MascheroniParser#base_construct_res.
    def exitBase_construct_res(self, ctx:MascheroniParser.Base_construct_resContext):
        pass


    # Enter a parse tree produced by MascheroniParser#base_construct_params.
    def enterBase_construct_params(self, ctx:MascheroniParser.Base_construct_paramsContext):
        pass

    # Exit a parse tree produced by MascheroniParser#base_construct_params.
    def exitBase_construct_params(self, ctx:MascheroniParser.Base_construct_paramsContext):
        pass


    # Enter a parse tree produced by MascheroniParser#inductive_construct_res.
    def enterInductive_construct_res(self, ctx:MascheroniParser.Inductive_construct_resContext):
        pass

    # Exit a parse tree produced by MascheroniParser#inductive_construct_res.
    def exitInductive_construct_res(self, ctx:MascheroniParser.Inductive_construct_resContext):
        pass


    # Enter a parse tree produced by MascheroniParser#inductive_construct_params.
    def enterInductive_construct_params(self, ctx:MascheroniParser.Inductive_construct_paramsContext):
        pass

    # Exit a parse tree produced by MascheroniParser#inductive_construct_params.
    def exitInductive_construct_params(self, ctx:MascheroniParser.Inductive_construct_paramsContext):
        pass


    # Enter a parse tree produced by MascheroniParser#StepShow.
    def enterStepShow(self, ctx:MascheroniParser.StepShowContext):
        pass

    # Exit a parse tree produced by MascheroniParser#StepShow.
    def exitStepShow(self, ctx:MascheroniParser.StepShowContext):
        pass


    # Enter a parse tree produced by MascheroniParser#StepAssignement.
    def enterStepAssignement(self, ctx:MascheroniParser.StepAssignementContext):
        pass

    # Exit a parse tree produced by MascheroniParser#StepAssignement.
    def exitStepAssignement(self, ctx:MascheroniParser.StepAssignementContext):
        pass


    # Enter a parse tree produced by MascheroniParser#StepDefine.
    def enterStepDefine(self, ctx:MascheroniParser.StepDefineContext):
        pass

    # Exit a parse tree produced by MascheroniParser#StepDefine.
    def exitStepDefine(self, ctx:MascheroniParser.StepDefineContext):
        pass


    # Enter a parse tree produced by MascheroniParser#StepWith.
    def enterStepWith(self, ctx:MascheroniParser.StepWithContext):
        pass

    # Exit a parse tree produced by MascheroniParser#StepWith.
    def exitStepWith(self, ctx:MascheroniParser.StepWithContext):
        pass


    # Enter a parse tree produced by MascheroniParser#StepIfs.
    def enterStepIfs(self, ctx:MascheroniParser.StepIfsContext):
        pass

    # Exit a parse tree produced by MascheroniParser#StepIfs.
    def exitStepIfs(self, ctx:MascheroniParser.StepIfsContext):
        pass


    # Enter a parse tree produced by MascheroniParser#ShowNoLabel.
    def enterShowNoLabel(self, ctx:MascheroniParser.ShowNoLabelContext):
        pass

    # Exit a parse tree produced by MascheroniParser#ShowNoLabel.
    def exitShowNoLabel(self, ctx:MascheroniParser.ShowNoLabelContext):
        pass


    # Enter a parse tree produced by MascheroniParser#ShowLabel.
    def enterShowLabel(self, ctx:MascheroniParser.ShowLabelContext):
        pass

    # Exit a parse tree produced by MascheroniParser#ShowLabel.
    def exitShowLabel(self, ctx:MascheroniParser.ShowLabelContext):
        pass


    # Enter a parse tree produced by MascheroniParser#IfThen.
    def enterIfThen(self, ctx:MascheroniParser.IfThenContext):
        pass

    # Exit a parse tree produced by MascheroniParser#IfThen.
    def exitIfThen(self, ctx:MascheroniParser.IfThenContext):
        pass


    # Enter a parse tree produced by MascheroniParser#IfElseThen.
    def enterIfElseThen(self, ctx:MascheroniParser.IfElseThenContext):
        pass

    # Exit a parse tree produced by MascheroniParser#IfElseThen.
    def exitIfElseThen(self, ctx:MascheroniParser.IfElseThenContext):
        pass


    # Enter a parse tree produced by MascheroniParser#ConditionNot.
    def enterConditionNot(self, ctx:MascheroniParser.ConditionNotContext):
        pass

    # Exit a parse tree produced by MascheroniParser#ConditionNot.
    def exitConditionNot(self, ctx:MascheroniParser.ConditionNotContext):
        pass


    # Enter a parse tree produced by MascheroniParser#ConditionComparison.
    def enterConditionComparison(self, ctx:MascheroniParser.ConditionComparisonContext):
        pass

    # Exit a parse tree produced by MascheroniParser#ConditionComparison.
    def exitConditionComparison(self, ctx:MascheroniParser.ConditionComparisonContext):
        pass


    # Enter a parse tree produced by MascheroniParser#ConditionEquality.
    def enterConditionEquality(self, ctx:MascheroniParser.ConditionEqualityContext):
        pass

    # Exit a parse tree produced by MascheroniParser#ConditionEquality.
    def exitConditionEquality(self, ctx:MascheroniParser.ConditionEqualityContext):
        pass


    # Enter a parse tree produced by MascheroniParser#ConditionParens.
    def enterConditionParens(self, ctx:MascheroniParser.ConditionParensContext):
        pass

    # Exit a parse tree produced by MascheroniParser#ConditionParens.
    def exitConditionParens(self, ctx:MascheroniParser.ConditionParensContext):
        pass


    # Enter a parse tree produced by MascheroniParser#named_expression.
    def enterNamed_expression(self, ctx:MascheroniParser.Named_expressionContext):
        pass

    # Exit a parse tree produced by MascheroniParser#named_expression.
    def exitNamed_expression(self, ctx:MascheroniParser.Named_expressionContext):
        pass


    # Enter a parse tree produced by MascheroniParser#InductiveExpression.
    def enterInductiveExpression(self, ctx:MascheroniParser.InductiveExpressionContext):
        pass

    # Exit a parse tree produced by MascheroniParser#InductiveExpression.
    def exitInductiveExpression(self, ctx:MascheroniParser.InductiveExpressionContext):
        pass


    # Enter a parse tree produced by MascheroniParser#InductiveNameName.
    def enterInductiveNameName(self, ctx:MascheroniParser.InductiveNameNameContext):
        pass

    # Exit a parse tree produced by MascheroniParser#InductiveNameName.
    def exitInductiveNameName(self, ctx:MascheroniParser.InductiveNameNameContext):
        pass


    # Enter a parse tree produced by MascheroniParser#InductiveInt.
    def enterInductiveInt(self, ctx:MascheroniParser.InductiveIntContext):
        pass

    # Exit a parse tree produced by MascheroniParser#InductiveInt.
    def exitInductiveInt(self, ctx:MascheroniParser.InductiveIntContext):
        pass


    # Enter a parse tree produced by MascheroniParser#InductiveName.
    def enterInductiveName(self, ctx:MascheroniParser.InductiveNameContext):
        pass

    # Exit a parse tree produced by MascheroniParser#InductiveName.
    def exitInductiveName(self, ctx:MascheroniParser.InductiveNameContext):
        pass


    # Enter a parse tree produced by MascheroniParser#inductive_names.
    def enterInductive_names(self, ctx:MascheroniParser.Inductive_namesContext):
        pass

    # Exit a parse tree produced by MascheroniParser#inductive_names.
    def exitInductive_names(self, ctx:MascheroniParser.Inductive_namesContext):
        pass


    # Enter a parse tree produced by MascheroniParser#EnteExpressionIntersection.
    def enterEnteExpressionIntersection(self, ctx:MascheroniParser.EnteExpressionIntersectionContext):
        pass

    # Exit a parse tree produced by MascheroniParser#EnteExpressionIntersection.
    def exitEnteExpressionIntersection(self, ctx:MascheroniParser.EnteExpressionIntersectionContext):
        pass


    # Enter a parse tree produced by MascheroniParser#EnteExpressionName.
    def enterEnteExpressionName(self, ctx:MascheroniParser.EnteExpressionNameContext):
        pass

    # Exit a parse tree produced by MascheroniParser#EnteExpressionName.
    def exitEnteExpressionName(self, ctx:MascheroniParser.EnteExpressionNameContext):
        pass


    # Enter a parse tree produced by MascheroniParser#EnteExpressionPrimitive.
    def enterEnteExpressionPrimitive(self, ctx:MascheroniParser.EnteExpressionPrimitiveContext):
        pass

    # Exit a parse tree produced by MascheroniParser#EnteExpressionPrimitive.
    def exitEnteExpressionPrimitive(self, ctx:MascheroniParser.EnteExpressionPrimitiveContext):
        pass


    # Enter a parse tree produced by MascheroniParser#EnteExpressionInvocation.
    def enterEnteExpressionInvocation(self, ctx:MascheroniParser.EnteExpressionInvocationContext):
        pass

    # Exit a parse tree produced by MascheroniParser#EnteExpressionInvocation.
    def exitEnteExpressionInvocation(self, ctx:MascheroniParser.EnteExpressionInvocationContext):
        pass


    # Enter a parse tree produced by MascheroniParser#invocation_params.
    def enterInvocation_params(self, ctx:MascheroniParser.Invocation_paramsContext):
        pass

    # Exit a parse tree produced by MascheroniParser#invocation_params.
    def exitInvocation_params(self, ctx:MascheroniParser.Invocation_paramsContext):
        pass


    # Enter a parse tree produced by MascheroniParser#IntExpressionAddSub.
    def enterIntExpressionAddSub(self, ctx:MascheroniParser.IntExpressionAddSubContext):
        pass

    # Exit a parse tree produced by MascheroniParser#IntExpressionAddSub.
    def exitIntExpressionAddSub(self, ctx:MascheroniParser.IntExpressionAddSubContext):
        pass


    # Enter a parse tree produced by MascheroniParser#IntExpressionID.
    def enterIntExpressionID(self, ctx:MascheroniParser.IntExpressionIDContext):
        pass

    # Exit a parse tree produced by MascheroniParser#IntExpressionID.
    def exitIntExpressionID(self, ctx:MascheroniParser.IntExpressionIDContext):
        pass


    # Enter a parse tree produced by MascheroniParser#IntExpressionParens.
    def enterIntExpressionParens(self, ctx:MascheroniParser.IntExpressionParensContext):
        pass

    # Exit a parse tree produced by MascheroniParser#IntExpressionParens.
    def exitIntExpressionParens(self, ctx:MascheroniParser.IntExpressionParensContext):
        pass


    # Enter a parse tree produced by MascheroniParser#IntExpressionMulDivMod.
    def enterIntExpressionMulDivMod(self, ctx:MascheroniParser.IntExpressionMulDivModContext):
        pass

    # Exit a parse tree produced by MascheroniParser#IntExpressionMulDivMod.
    def exitIntExpressionMulDivMod(self, ctx:MascheroniParser.IntExpressionMulDivModContext):
        pass


    # Enter a parse tree produced by MascheroniParser#IntExpressionInt.
    def enterIntExpressionInt(self, ctx:MascheroniParser.IntExpressionIntContext):
        pass

    # Exit a parse tree produced by MascheroniParser#IntExpressionInt.
    def exitIntExpressionInt(self, ctx:MascheroniParser.IntExpressionIntContext):
        pass


    # Enter a parse tree produced by MascheroniParser#int_name.
    def enterInt_name(self, ctx:MascheroniParser.Int_nameContext):
        pass

    # Exit a parse tree produced by MascheroniParser#int_name.
    def exitInt_name(self, ctx:MascheroniParser.Int_nameContext):
        pass


    # Enter a parse tree produced by MascheroniParser#name_name.
    def enterName_name(self, ctx:MascheroniParser.Name_nameContext):
        pass

    # Exit a parse tree produced by MascheroniParser#name_name.
    def exitName_name(self, ctx:MascheroniParser.Name_nameContext):
        pass


    # Enter a parse tree produced by MascheroniParser#expression_name.
    def enterExpression_name(self, ctx:MascheroniParser.Expression_nameContext):
        pass

    # Exit a parse tree produced by MascheroniParser#expression_name.
    def exitExpression_name(self, ctx:MascheroniParser.Expression_nameContext):
        pass


    # Enter a parse tree produced by MascheroniParser#typed_name.
    def enterTyped_name(self, ctx:MascheroniParser.Typed_nameContext):
        pass

    # Exit a parse tree produced by MascheroniParser#typed_name.
    def exitTyped_name(self, ctx:MascheroniParser.Typed_nameContext):
        pass


    # Enter a parse tree produced by MascheroniParser#typed_int_name.
    def enterTyped_int_name(self, ctx:MascheroniParser.Typed_int_nameContext):
        pass

    # Exit a parse tree produced by MascheroniParser#typed_int_name.
    def exitTyped_int_name(self, ctx:MascheroniParser.Typed_int_nameContext):
        pass


    # Enter a parse tree produced by MascheroniParser#typed_name_name.
    def enterTyped_name_name(self, ctx:MascheroniParser.Typed_name_nameContext):
        pass

    # Exit a parse tree produced by MascheroniParser#typed_name_name.
    def exitTyped_name_name(self, ctx:MascheroniParser.Typed_name_nameContext):
        pass



del MascheroniParser