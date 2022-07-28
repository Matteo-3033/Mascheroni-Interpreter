import ASTree.nodes.ExpressionNodes as exprs


class IntNode(exprs.IntExpressionNode):
    """
    Nodo che rappresenta un valore intero e che quando visitato lo restituisce
    """
    def __init__(
        self,
        number: int
    ):

        super().__init__()
        self.value = int(number)
        self.nodeName = "IntNode"


    def visit(self, interpreter):
        return self.value, "int"


class MulDivModNode(exprs.BinaryOperatorNode, exprs.IntExpressionNode):
    """
    Nodo che rappresenta operazioni di moltiplicazione, divisione e modulo tra espressioni intere.
    """
    def __init__(
        self,
        op: str,
        lhsIntExpression: exprs.IntExpressionNode,
        rhsIntExpression: exprs.IntExpressionNode
    ):
    
        if op not in {"*", "/", "%"}:
            raise ValueError(f'Operatore {op} non valido.\nPossibili operatori: "*", "/", "%".')

        if not isinstance(lhsIntExpression, exprs.IntExpressionNode):
            raise TypeError(f"lhsIntExpression deve essere di tipo IntExpressionNode, non {type(lhsIntExpression)}.")
        if not isinstance(rhsIntExpression, exprs.IntExpressionNode):
            raise TypeError(f"rhsIntExpression deve essere di tipo IntExpressionNode, non {type(rhsIntExpression)}.")
        
        super().__init__(op, lhsIntExpression, rhsIntExpression)
        self.nodeName = "MulDivModNode"
    
    
    def visit(self, interpreter):
        # Calcolo del valore degli operandi:
        left, leftType = self.lhsExpressionTree.visit(interpreter)
        right, rightType = self.rhsExpressionTree.visit(interpreter)

        if leftType != "int" or rightType != "int":
            raise TypeError(
                f"È possibile eseguire operazioni algebriche solamente tra interi, non tra {leftType} e {rightType}:\n{left} {self.op} {right}"
            )
        
        # Non è possibile dividere per 0:
        if right == 0 and self.op != "*":
            raise ZeroDivisionError(
                f"Impossibile dividere per 0:\n{left} {self.op} {right}"
            )
        
        # Applicazione dell'opeatore agli operandi:
        return interpreter.opDT[self.op](left, right), "int"


class AddSubNode(exprs.BinaryOperatorNode, exprs.IntExpressionNode):
    """
    Nodo che rappresenta operazioni di addizione e sottrazione tra espressioni intere.
    """
    def __init__(
        self,
        op: str,
        lhsIntExpression: exprs.IntExpressionNode,
        rhsIntExpression: exprs.IntExpressionNode
    ):
    
        if op not in {"+", "-"}:
            raise ValueError(
                f'Operatore {op} non valido.\nPossibili operatori: "+", "-".'
            )

        if not isinstance(lhsIntExpression, exprs.IntExpressionNode):
            raise TypeError(f"lhsIntExpression deve essere di tipo IntExpressionNode, non {type(lhsIntExpression)}.")
        if not isinstance(rhsIntExpression, exprs.IntExpressionNode):
            raise TypeError(f"rhsIntExpression deve essere di tipo IntExpressionNode, non {type(rhsIntExpression)}.")
        
        super().__init__(op, lhsIntExpression, rhsIntExpression)
        self.nodeName = "AddSubNode"
    
    
    def visit(self, interpreter):
        # Calcolo del valore degli operandi:
        left, leftType = self.lhsExpressionTree.visit(interpreter)
        right, rightType = self.rhsExpressionTree.visit(interpreter)
        
        if leftType != "int" or rightType != "int":
            raise TypeError(
                f"È possibile eseguire operazioni algebriche solamente tra interi, non tra {leftType} e {rightType}:\n{left} {self.op} {right}"
            )
        
        # Applicazione dell'opeatore agli operandi:
        return interpreter.opDT[self.op](left, right), "int"
    