from abc import ABC, abstractmethod
from typing import List


class TreeNode(ABC):
    """
    Nodo astratto di un albero che salva il proprio nome e una lista di nodi figli.
    Tutte le classi figlie devono sovrascrivere il metodo visit(Interpreter) affinché
    quando invocato passandogli in input un oggetto della classe Interpreter esegua
    il codice corrispondente all'albero che ha per radice il nodo su cui è stato invocato
    il metodo eventualmente ricavando informazioni necessarie all'invocazione invocando
    sé stesso sui figli del nodo.
    """
    def __init__(
        self,
        children: list = list()
    ):
        self.children = children
        self.nodeName = "AbstractTreeNode"


    @property
    def childrenNum(self):
        """Restituisc il numero di nodi figli del nodo."""
        return len(self.children)


    @abstractmethod
    def visit(self, interpreter):
        """
        Metodo di visita dell'albero con radice questo nodo.
        Ogni classe che eredita da TreeNode deve implementare questo metodo eventualmente
        invocando il metodo visit dei suoi nodi figli.
        """
        raise NotImplementedError()


    def __repr__(self):
        return self.__hierarchicalRepresentation()


    def __hierarchicalRepresentation(self, ended: List[bool]= list()):
        """Restituisce una rappresentazione gerarchica dell'albero sotto forma di stringa"""  
        pre = ""
        for i in ended[:-1]:
            if i: pre += "   "
            else: pre += "│  "
        
        res = pre + ("" if len(ended) == 0 else "└──" if ended[-1] else "├──") + self.nodeName + '\n'
        
        if self.childrenNum > 0:
            for child in self.children[:-1]:
                res += child.__hierarchicalRepresentation(ended + [False])
            res += self.children[-1].__hierarchicalRepresentation(ended + [True])

        return res
