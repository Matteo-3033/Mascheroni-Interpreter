import ASTree.nodes.InductiveConstruct as ic
import ASTree.nodes.IntExpressionNodes as ints
import ASTree.nodes.ExpressionNodes as exprs
import ASTree.nodes.TreeNode as tree

from abc import abstractmethod
from typing import List


class AbstractNameNode(exprs.EnteExpressionNode):
    """
    Classe astratta da cui ereditano tutti i nodi che rappresentano un nome.
    Tutte le classi figlie devono sovrascivere il metodo symbol(Interpreter) per restituire il
    corrispondente nome salvato in memoria e il metodo baseSymbol per restituire il nome privo
    di un eventuale pedice.
    L'implementazione base del metodo di visita restituisce il valore e il tipo associati
    al nome in memoria.
    """
    def __init__(
        self,
        children: list = list()
    ):

        super().__init__(children)
        self.nodeName = "AbstractNameNode"
    

    @abstractmethod
    def symbol(self, interpreter):
        """
        Restituisce il simbolo valutato.
        Per un nome semplice questo corrisponde semplicemente al nome, per
        quelli composti il pedice è sostituito con l'intero corrispondente in base
        ai valori salvati in memoria.
        """
        raise NotImplementedError()
    

    @property
    @abstractmethod
    def baseSymbol(self):
        """
        Restituisce il nome base del nodo.
        I NameNode restituiscono semplicemente il loro attributo name,
        mentre i nomi composti il loro nome privo di pedice.
        """
        raise NotImplementedError()


    @abstractmethod
    def visit(self, interpreter):
        value, valueType = interpreter.actRecord.getValue(self.symbol(interpreter))
        if value is None:
            raise NameError(f"Simbolo {self.symbol(interpreter)} non definito.")
        else:
            return value, valueType


class NameNode(AbstractNameNode, exprs.IntExpressionNode):
    """
    Nodo che rappresenta un nome semplice composto da soli caratteri alfabetici.
    Un NameNode può essere sia un'espressione intera sia un'espressione sugli enti,
    a seconda del valore ad esso associato in memoria.
    """
    def __init__(
        self,
        name: str
    ):
    
        name = str(name)
        if len(name) == 0:
            raise ValueError("name non può essere vuoto.")
        if not name.isalpha():
            raise ValueError("name deve contenere solamente caratteri alfabetici.")
 
        super().__init__()
        self.name = name
        self.nodeName = "NameNode"


    def symbol(self, interpreter):
        return self.baseSymbol
    

    @property
    def baseSymbol(self):
        return self.name


    def visit(self, interpreter):
        return super().visit(interpreter)
        

class AbstractComposedNameNode(AbstractNameNode):
    """
    Classe astratta che rappresenta nomi con associato un pedice.
    Il nome vero e proprio deve essere un oggetto di tipo NameNode, mentre il pedice
    di tipo IntExpressionNode perché quando visitato restituisca un intero.
    L'implementazione base del metodo di visit controlla se al simbolo nomeBase_valorePedice
    non è già stato associato un valore in memoria e nel caso lo restituisce; altrimenti se
    al nome base è associato un oggetto di tipo InductiveConstruct lo invoca per il valore
    del pedice.
    """
    def __init__(
        self,
        lhs: NameNode,
        rhs: exprs.IntExpressionNode
    ):
    
        if not isinstance(lhs, NameNode):
            raise TypeError(f"NameNode expected, given {type(lhs)}")
        if not isinstance(rhs, exprs.IntExpressionNode):
            raise TypeError(f"IntExpressionNode expected, given {type(rhs)}")
            
        super().__init__([lhs, rhs])
        self.nodeName = "AbstractComposedNameNode"


    @abstractmethod
    def symbol(self, interpreter):
        rhs, rhsType = self.rhsTree.visit(interpreter)
        if rhsType != "int":
            raise TypeError(
                f"La valutazione del livello di induzione di {self.baseSymbol} deve restituire un intero, non {rhsType}."
            )
        return self.lhsTree.symbol(interpreter) + '_' + str(rhs)


    @property
    def baseSymbol(self):
        return self.lhsTree.name
        

    @property
    def lhsTree(self):
        return self.children[0]


    @property
    def rhsTree(self):
        return self.children[1]


    @abstractmethod
    def visit(self, interpreter):
        # Se il nome completo è già salvato in memoria viene restituito direttamente:
        value, valueType = interpreter.actRecord.getValue(self.symbol(interpreter))

        if value:
            return value, valueType
        else:
            # Altrimenti se al nome base è associato un costrutto induttivo valuto il costrutto
            # per il pedice corrispondente.
            inductiveName, _ = interpreter.actRecord.getValue(self.baseSymbol)
            
            if not inductiveName:
                raise NameError(f"Simbolo {self.baseSymbol} non definito.")
            elif isinstance(inductiveName, ic.InductiveConstruct):
                # Invoco il construct induttivo a partire dal livello indicato dal pedice:
                n, _ = self.rhsTree.visit(interpreter)

                # Il livello di induzione non può essere maggiore di quello attuale:
                if inductiveName.currentLevel and n >= inductiveName.currentLevel:
                    raise RecursionError(
                        "I construct induttivi possono essere definiti solamente in funzione di enti di livello inferiore del corrente."
                    )
                
                return inductiveName(interpreter, n)
            else:
                raise TypeError(f"Al simbolo {self.lhsTree.symbol(interpreter)} non è associato alcun ente induttivo.")
        

class IntNameNode(AbstractComposedNameNode):
    """
    Nodo che rappresenta un nome composto nella forma nome_intero.
    """
    def __init__(
        self, 
        lhs: str,
        rhs: int
    ):
        super().__init__(
            NameNode(lhs),
            ints.IntNode(rhs)
        )
        self.nodeName = "IntNameNode"


    def symbol(self, interpreter):
        return super().symbol(interpreter)


    def visit(self, interpreter):
        return super().visit(interpreter)


class NameNameNode(AbstractComposedNameNode):
    """
    Nodo che rappresenta un nome composto nella forma nome_nome.
    """
    def __init__(
        self,
        lhs: str,
        rhs: str
    ):
        super().__init__(
            NameNode(lhs),
            NameNode(rhs)
        )
        self.nodeName = "NameNameNode"


    def symbol(self, interpreter):
        return super().symbol(interpreter)
        

    def visit(self, interpreter):
        return super().visit(interpreter)


class ExpressionNameNode(AbstractComposedNameNode):
    """
    Nodo che rappresenta un nome composto nella forma nome_(espressione intera).
    """
    def __init__(
        self,
        lhs: str,
        rhs: exprs.IntExpressionNode
    ):
        super().__init__(
            NameNode(lhs),
            rhs
        )
        self.nodeName = "ExpressionNameNode"


    def symbol(self, interpreter):
        return super().symbol(interpreter)


    def visit(self, interpreter):
        return super().visit(interpreter)


class AbstractTypedNameNode(tree.TreeNode):
    """
    Classe astratta che rappresenta un nome a cui è associato un tipo.
    Il tipo può essere uno tra "point", "segment", "ray", "line" e "circle".
    """
    def __init__(
        self,
        nameType: str,
        name: AbstractNameNode
    ):
        if nameType not in {"point", "segment", "ray", "line", "circle"}:
            raise ValueError(
                f'Tipo {nameType} non valido.\nPossibili valori: "point", "segment", "ray", "line", "circle".'
            )
        
        if not isinstance(name, AbstractNameNode):
            raise TypeError(f"name deve essere di tipo AbstractNameNode, non {type(name)}.")
        
        super().__init__([name])
        self.type = nameType
        self.nodeName = "AbstractTypedNameNode"


    @property
    def nameTree(self):
        return self.children[0]


    def visit(self, interpreter):
        return super().visit(interpreter)


class TypedNameNode(AbstractTypedNameNode):
    """
    Nodo che rappresenta un nome semplice tipizzato.
    """
    def __init__(
        self,
        nameType: str,
        name: NameNode
    ):
        if not isinstance(name, NameNode):
            raise TypeError(f"name deve essere di tipo NameNode, non {type(name)}.")
        
        super().__init__(nameType, name)
        self.nodeName = "TypedNameNode"


    def visit(self, interpreter):
        return super().visit(interpreter)


class TypedIntNameNode(AbstractTypedNameNode):
    """
    Nodo che rappresenta un nome_int tipizzato.
    """
    def __init__(
        self,
        nameType: str,
        name: IntNameNode
    ):
        if not isinstance(name, IntNameNode):
            raise TypeError(f"name deve essere di tipo IntNameNode, non {type(name)}.")
        
        super().__init__(nameType, name)
        self.nodeName = "TypedIntNameNode"


    def visit(self, interpreter):
        return super().visit(interpreter)


class TypedNameNameNode(AbstractTypedNameNode):
    """
    Nodo che rappresenta un nome_nome tipizzato.
    """
    def __init__(
        self,
        nameType: str,
        name: NameNameNode
    ):
        if not isinstance(name, NameNameNode):
            raise TypeError(f"name deve essere di tipo NameNameNode, non {type(name)}.")
    
        super().__init__(nameType, name)
        self.nodeName = "TypedNameNameNode"


    def visit(self, interpreter):
        return super().visit(interpreter)


class NamesNode(exprs.ListNode):
    """
    Nodo i cui figli sono tutti di tipo AbstractNameNode.
    """
    def __init__(
        self,
        names: List[AbstractNameNode]
    ):
        super().__init__(names)
        
        for name in names:
            if not isinstance(name, AbstractNameNode):
                raise TypeError(f"names deve essere una lista di AbstractNameNode, non {type(name)}.")
        
        self.nodeName = "NamesNode"


    def visit(self, interpreter):
        raise NotImplementedError()
        