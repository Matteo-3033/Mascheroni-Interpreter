from Grammatica.MascheroniParser import MascheroniParser
from Grammatica.MascheroniVisitor import MascheroniVisitor

from .nodes.Nodes import *


class ASTVisitor(MascheroniVisitor):
    """
    Implementazione dell'interfaccia MascheroniVisitor che restituisce l'AST
    relativo all'albero di parsing su cui è eseguita la visita.
    """
    def visitStart(self, ctx:MascheroniParser.StartContext):
        approximate = False
        if ctx.APPROXIMATE(): approximate = True
        
        return Ast(
            [self.visit(child) for child in ctx.construct()],
            approximate
        )
    
    
    # Construct:

    def visitBaseConstruct(self, ctx:MascheroniParser.BaseConstructContext):
        results = None
        if ctx.base_construct_res():
            results = self.visit(ctx.base_construct_res())

        params = self.visit(ctx.base_construct_params())
        
        return BaseConstructNode(
            ctx.NAME().getText(),
            StepsNode([self.visit(step) for step in ctx.step()]),
            params,
            results            
        )

    def visitInductiveConstruct(self, ctx:MascheroniParser.InductiveConstructContext):
        results = self.visit(ctx.inductive_construct_res())
        params = self.visit(ctx.inductive_construct_params())
        
        return InductiveConstructNode(
            ctx.NAME().getText(),
            StepsNode([self.visit(step) for step in ctx.step()]),
            params,
            results
        )

    def visitBase_construct_res(self, ctx:MascheroniParser.Base_construct_resContext):
        return BaseConstructResultsNode(
            [self.visit(child) for child in ctx.typed_name()]
        )

    def visitBase_construct_params(self, ctx:MascheroniParser.Base_construct_paramsContext):
        return BaseConstructParamsNode(
            [self.visit(child) for child in ctx.typed_name()]
        )
    
    def visitInductive_construct_res(self, ctx:MascheroniParser.Inductive_construct_resContext):
        return InductiveConstructResultsNode(
            [self.visit(child) for child in ctx.typed_name_name()]
        )

    def visitInductive_construct_params(self, ctx:MascheroniParser.Inductive_construct_paramsContext):
        return InductiveConstructParamsNode(
            [self.visit(child) for child in ctx.children
                if child.getText() != MascheroniParser.literalNames[MascheroniParser.SEP][1:-1]]
        )

    
    # Steps:
    
    def visitStepAssignement(self, ctx:MascheroniParser.StepAssignementContext):
        return AssignementNode(
            NameNode(ctx.NAME().getText()),
            self.visit(ctx.int_expression())
        )

    def visitStepWith(self, ctx:MascheroniParser.StepWithContext):
        return WithNode(
            NamedExpressionsNode([self.visit(expression) for expression in ctx.named_expression()]),
            StepsNode([self.visit(step) for step in ctx.step()])
        )


    # Show:

    def visitShowNoLabel(self, ctx:MascheroniParser.ShowNoLabelContext):
        return DrawNode()
    
    def visitShowLabel(self, ctx:MascheroniParser.ShowLabelContext):
        return DrawLabelNode()

    
    # If-then / if-then-else:

    def visitIfThen(self, ctx:MascheroniParser.IfThenContext):
        return IfThenNode(
            self.visit(ctx.condition()),
            StepsNode([self.visit(step) for step in ctx.step()])
        )
    
    def visitIfElseThen(self, ctx:MascheroniParser.IfElseThenContext):
        _, _, _, *steps, _ = ctx.children
        # if, condition, then, (steps+ else steps+), fi
        
        for i in range(len(steps)):
            if steps[i].getText() == "else":
                elsePos = i
        
        return IfThenElseNode(
            self.visit(ctx.condition()),
            StepsNode([self.visit(step) for step in ctx.step()[:elsePos]]),
            StepsNode([self.visit(step) for step in ctx.step()[elsePos:]])
        )
 
    def visitConditionNot(self, ctx:MascheroniParser.ConditionNotContext):
        return ConditionNotNode(self.visit(ctx.expr))
    
    def visitConditionComparison(self, ctx:MascheroniParser.ConditionComparisonContext):
        return ConditionComparisonNode(
            ctx.op.text,
            self.visit(ctx.left),
            self.visit(ctx.right)
        )

    def visitConditionEquality(self, ctx:MascheroniParser.ConditionEqualityContext):
        return ConditionEqualityNode(
            ctx.op.text,
            self.visit(ctx.left),
            self.visit(ctx.right)
        )
    
    def visitConditionParens(self, ctx:MascheroniParser.ConditionParensContext):
        return self.visit(ctx.condition())


    # Define:
    
    def visitStepDefine(self, ctx:MascheroniParser.StepDefineContext):
        return DefineNode(
            self.visit(ctx.named_expression())            
        )

    def visitNamed_expression(self, ctx:MascheroniParser.Named_expressionContext):
        upto = None
        if ctx.int_expression(): upto = self.visit(ctx.int_expression())
        
        if upto is None:
            return NamedExpressionNode(
                self.visit(ctx.ente_expression()),
                self.visit(ctx.inductive_names())
            )
        else:
            return UpToNamedExpressionNode(
                self.visit(ctx.ente_expression()),
                self.visit(ctx.inductive_names()),
                upto
            )

    def visitInductiveName(self, ctx:MascheroniParser.InductiveNameContext):
        return NameNode(ctx.NAME().getText())
    
    def visitInductive_names(self, ctx:MascheroniParser.Inductive_namesContext):
        return NamesNode(
            [self.visit(child) for child in ctx.inductive_name()]
        )


    # Ente expressions:

    def visitEnteExpressionIntersection(self, ctx:MascheroniParser.EnteExpressionIntersectionContext):
        return IntersectionNode(
            ctx.op.text,
            self.visit(ctx.left),
            self.visit(ctx.right)
        )
    
    def visitEnteExpressionPrimitive(self, ctx:MascheroniParser.EnteExpressionPrimitiveContext):
        return PrimitiveNode(
            ctx.Type.text,
            self.visit(ctx.ente_expression(0)),
            self.visit(ctx.ente_expression(1))
        )
    
    def visitEnteExpressionInvocation(self, ctx:MascheroniParser.EnteExpressionInvocationContext):
        return InvocationNode(
            ctx.NAME().getText(),
            [self.visit(child) for child in ctx.invocation_params().ente_expression()]
        )

    
    # Int expressions:
    
    def visitIntExpressionMulDivMod(self, ctx:MascheroniParser.IntExpressionMulDivModContext):
        return MulDivModNode(
            ctx.op.text,
            self.visit(ctx.left),
            self.visit(ctx.right)
        )
    
    def visitIntExpressionAddSub(self, ctx:MascheroniParser.IntExpressionAddSubContext):
        return AddSubNode(
            ctx.op.text,
            self.visit(ctx.left),
            self.visit(ctx.right)
        )
    
    def visitIntExpressionParens(self, ctx:MascheroniParser.IntExpressionParensContext):
        return self.visit(ctx.int_expression())
    
    def visitIntExpressionInt(self, ctx:MascheroniParser.IntExpressionIntContext):
        return IntNode(int(ctx.INT().getText()))
    
    def visitIntExpressionID(self, ctx:MascheroniParser.IntExpressionIntContext):
        return NameNode(ctx.NAME().getText())
    
    
    # Names:
    
    def visitInt_name(self, ctx:MascheroniParser.Int_nameContext):
        return IntNameNode(
            ctx.NAME().getText(),
            ctx.INT().getText()
        )
    
    def visitName_name(self, ctx:MascheroniParser.Name_nameContext):
        return NameNameNode(
            ctx.NAME(0).getText(),
            ctx.NAME(1).getText()
        )
    
    def visitExpression_name(self, ctx:MascheroniParser.Expression_nameContext):
        return ExpressionNameNode(
            ctx.NAME().getText(),
            self.visit(ctx.int_expression())
        )
  
    def visitTyped_name(self, ctx:MascheroniParser.Typed_nameContext):
        return TypedNameNode(
            ctx.Type.text,
            NameNode(ctx.NAME().getText())
        )
    
    def visitTyped_int_name(self, ctx:MascheroniParser.Typed_int_nameContext):
        return TypedIntNameNode(
            ctx.Type.text,
            self.visit(ctx.int_name())
        )
        
    def visitTyped_name_name(self, ctx:MascheroniParser.Typed_name_nameContext):
        return TypedNameNameNode(
            ctx.Type.text,
            self.visit(ctx.name_name())
        )
    