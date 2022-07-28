import ASTree.nodes.TreeNode as tree

from abc import abstractmethod
from typing import List


class AbstractExpressionNode(tree.TreeNode):
    """
    Nodo che rappresenta un'espressione astratta che quando visitata
    restituisce un risultato e il suo tipo.
    """
    def __init__(
        self,
        children: list = list()
    ):

        super().__init__(children)
        self.nodeName = "AbstractExpressionNode"


class EnteExpressionNode(AbstractExpressionNode):
    """
    Nodo astratto che rappresenta espressioni sugli enti.
    """
    def __init__(
        self,
        children: list = list()
    ):

        super().__init__(children)
        self.nodeName = "EnteExpressionNode"


class IntExpressionNode(AbstractExpressionNode):
    """
    Nodo astratto che rappresenta espressioni intere.
    """
    def __init__(
        self,
        children: list = list()
    ):

        super().__init__(children)
        self.nodeName = "IntExpressionNode"


class ConditionNode(AbstractExpressionNode):
    """
    Nodo astratto che rappresenta una condizione booleana.
    """    
    def __init__(self, children: list = list()):
        super().__init__(children)
        self.nodeName = "ConditionNode"


class UnaryOperatorNode(tree.TreeNode):
    """
    Nodo astratto che rappresenta operatori unari.
    """
    def __init__(
        self,
        op: str,
        expression: AbstractExpressionNode
    ):
        if not isinstance(expression, AbstractExpressionNode):
            raise TypeError(f"expressione deve essere di tipo AbstractExpressionNode, non {type(expression)}")
        
        super().__init__([expression])

        self.op = str(op)
        self.nodeName = "UnaryOperatorNode"
    

    @property
    def expressionTree(self):
        return self.children[0]


class BinaryOperatorNode(tree.TreeNode):
    """
    Nodo astratto che rappresenta operatori binari.
    """
    def __init__(
        self,
        op: str,
        lhsExpression: AbstractExpressionNode,
        rhsExpression: AbstractExpressionNode
    ):

        if not isinstance(lhsExpression, AbstractExpressionNode):
            raise TypeError(f"lhsExpression deve essere di tipo AbstractExpressionNode, non {type(lhsExpression)}.")
        if not isinstance(rhsExpression, AbstractExpressionNode):
            raise TypeError(f"rhsExpression deve essere di tipo AbstractExpressionNode, non {type(rhsExpression)}.")
        
        super().__init__([lhsExpression, rhsExpression])

        self.op = str(op)
        self.nodeName = "BinaryOperatorNode"
    

    @property
    def lhsExpressionTree(self):
        return self.children[0]


    @property
    def rhsExpressionTree(self):
        return self.children[1]


class ListNode(tree.TreeNode):
    """
    Classe astratta che rappresenta nodi che salvano solamente un insieme di figli
    di uno stesso tipo. L'implementazione base del metodo visit(interpreter) si limita
    a reinvocare sé stesso su tutti i figli in ordine.
    """
    def __init__(
        self,
        names: List[tree.TreeNode]
    ):
    
        if not isinstance(names, list):
            raise TypeError("names deve essere una lista di TreeNode.")
        if len(names) == 0:
            raise ValueError("La lista names deve contenere almeno un elemento.")

        super().__init__(names)
        self.nodeName = "ListNode"


    @abstractmethod
    def visit(self, interpreter):
        for child in self.children:
            child.visit(interpreter)
