import ASTree.nodes.ExpressionNodes as exprs


class ConditionNotNode(exprs.UnaryOperatorNode, exprs.ConditionNode):
    """
    Nodo che rappresenta l'operatore unario booleano ! applicato a una condizione.
    Ha per unico figlio un nodo che rappresenta la condizione negata.
    """
    def __init__(self, condition: exprs.ConditionNode):
        if not isinstance(condition, exprs.ConditionNode):
            raise TypeError(f"condition deve essere di tipo ConditionNode, non {type(condition)}.")

        super().__init__("!", condition)
        self.nodeName = "ConditionNotNode"


    def visit(self, interpreter):
        # Calcolo del valore della condizione:
        expr, exprType = self.expressionTree.visit(interpreter)
        # Applicazione dell'operatore ! alla condizione:
        return interpreter.opDT[self.op](expr), exprType
    


class ConditionComparisonNode(exprs.BinaryOperatorNode, exprs.ConditionNode):
    """
    Nodo che rappresenta gli operatori binari booleani di confronto <, <=, > e >= applicati a due espressioni intere.
    Ha come figli due nodi che rappresentano l'operando destro e sinitro dell'operatore.
    """
    def __init__(
        self,
        op: str,
        lhsIntExpression: exprs.IntExpressionNode,
        rhsIntExpression: exprs.IntExpressionNode
    ):
        if op not in {"<", "<=", ">", ">="}:
            raise ValueError(
                f'Operatore {op} non valido.\nPossibili operatori: "<", "<=", ">", ">=".'
            )

        if not isinstance(lhsIntExpression, exprs.IntExpressionNode):
            raise TypeError(f"lhsIntExpression deve essere di tipo IntExpressionNode, non {type(lhsIntExpression)}.")
        if not isinstance(rhsIntExpression, exprs.IntExpressionNode):
            raise TypeError(f"rhsIntExpression deve essere di tipo IntExpressionNode, non {type(rhsIntExpression)}.")
        
        super().__init__(op, lhsIntExpression, rhsIntExpression)
        self.nodeName = "ConditionComparisonNode"


    def visit(self, interpreter):
        # Calcolo del valore degli operandi:
        left, leftType = self.lhsExpressionTree.visit(interpreter)
        right, rightType = self.rhsExpressionTree.visit(interpreter)
        
        if leftType != "int" or rightType != "int":
            raise TypeError(
                f"È possibile confrontare solamente interi, non {leftType} e {rightType}:\n{left} {self.op} {right}"
            )
        
        # Applicazione dell'operatore sugli operandi:
        return interpreter.opDT[self.op](left, right), "bool"
    


class ConditionEqualityNode(exprs.BinaryOperatorNode, exprs.ConditionNode):
    """
    Nodo che rappresenta gli operatori binari booleani di confronto == e != applicati a due interi.
    Ha come figli due nodi che rappresentano l'operando destro e sinitro dell'operatore.
    """
    def __init__(
        self,
        op: str,
        lhsIntExpression: exprs.IntExpressionNode,
        rhsIntExpression: exprs.IntExpressionNode
    ):
        if op not in {"==", "!="}:
            raise ValueError(
                f'Operatore {op} non valido.\nPossibili operatori: "==", "!=".'
            )

        if not isinstance(lhsIntExpression, exprs.IntExpressionNode):
            raise TypeError(f"lhsIntExpression deve essere di tipo IntExpressionNode, non {type(lhsIntExpression)}.")
        if not isinstance(rhsIntExpression, exprs.IntExpressionNode):
            raise TypeError(f"rhsIntExpression deve essere di tipo IntExpressionNode, non {type(rhsIntExpression)}.")
        
        super().__init__(op, lhsIntExpression, rhsIntExpression)
        self.nodeName = "ConditionEqualityNode"
        

    def visit(self, interpreter):
        # Calcolo del valore degli operandi:
        left, leftType = self.lhsExpressionTree.visit(interpreter)
        right, rightType = self.rhsExpressionTree.visit(interpreter)

        if leftType != "int" or rightType != "int":
            raise TypeError(
                f"È possibile uguagliare solamente interi, non {leftType} e {rightType}:\n{left} {self.op} {right}"
            )
        
        # Applicazione dell'operatore sugli operandi:
        return interpreter.opDT[self.op](left, right), "bool"
