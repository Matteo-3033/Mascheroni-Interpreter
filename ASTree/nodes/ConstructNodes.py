import ASTree.nodes.StepNodes as steps
import ASTree.nodes.NameNodes as names
import ASTree.nodes.ExpressionNodes as exprs
import ASTree.nodes.TreeNode as tree

from abc import abstractmethod
from typing import List


class AbstractConstructResultsNode(exprs.ListNode):
    """
    Nodo astratto che salva i nomi e i tipi dei valori di ritorno di un construct.
    Il metodo di visita di questo nodo non è implementato poiché utilizzato prevalentemente
    per accedere ai risultati di un construct.
    """
    def __init__(self, typedNames: List[names.AbstractTypedNameNode]):
        super().__init__(typedNames)
        self.nodeName = "AbstractConstructResultsNode"


    def visit(self, interpreter):
        raise NotImplementedError()


class BaseConstructResultsNode(AbstractConstructResultsNode):
    """
    AbstractConstructResultsNode per construct non induttivi.
    Tutti i suoi figli appartengono alla classe TypedNameNode e rappresentano un nome semplice (senza pedice) tipizzato.
    """
    def __init__(self, typedNames: List[names.TypedNameNode]):
        super().__init__(typedNames)
        
        for typedName in typedNames:
            if not (isinstance(typedName, names.TypedNameNode)):
                raise TypeError(f"typedNames deve essere una lista di TypedNameNode, non {type(typedName)}.")

        self.nodeName = "BaseConstructResultsNode"


    def visit(self, interpreter):
        return super().visit(interpreter)


class InductiveConstructResultsNode(AbstractConstructResultsNode):
    """
    AbstractConstructResultsNode per construct induttivi.
    Tutti i suoi figli appartengono alla classe TypedNameNode e rappresentano un nome semplice (senza pedice) tipizzato.
    """
    def __init__(self, typedNames: List[names.TypedNameNameNode]):
        super().__init__(typedNames)
        
        n = None
        for typedName in typedNames:
            if not (isinstance(typedName, names.TypedNameNameNode)):
                raise TypeError(f"typedNames deve essere una lista di TypedNameNode, non {type(typedName)}.")
            if not n:
                n = typedName.nameTree.rhsTree.baseSymbol
            elif n != typedName.nameTree.rhsTree.baseSymbol:
                raise ValueError("Tutti i risultati di un construct induttivo devono avere lo stesso pedice.")

        self.nodeName = "InductiveConstructResultNode"
    
    
    def visit(self, interpreter):
        return super().visit(interpreter)


class AbstractConstructParamsNode(exprs.ListNode):
    """
    Nodo astratto che salva i nomi e i tipi dei valori dei parametri di un construct.
    Il metodo di visita di questo nodo non è implementato poiché utilizzato prevalentemente
    per accedere ai parametri di un construct.
    """
    def __init__(self, typedNames: List[names.AbstractTypedNameNode]):
        super().__init__(typedNames)
        self.nodeName = "AbstractConstructParamsNode"


    def visit(self, interpreter):
        raise NotImplementedError()


class BaseConstructParamsNode(AbstractConstructParamsNode):
    """
    AbstractConstructParamsNode per construct non induttivi.
    Tutti i suoi figli appartengono alla classe TypedNameNode e rappresentano un nome semplice (senza pedice) tipizzato.
    """
    def __init__(self, typedNames: List[names.TypedNameNode]):
        super().__init__(typedNames)

        for typedName in typedNames:
            if not isinstance(typedName, names.TypedNameNode):
                raise TypeError(f"typedNames deve essere una lista di TypedNameNode, non {type(typedName)}.")

        self.nodeName = "BaseConstructParamsNode"
        

    def visit(self, interpreter):
        return super().visit(interpreter)
    

class InductiveConstructParamsNode(AbstractConstructParamsNode):
    """
    AbstractConstructParamsNode per construct induttivi.
    Tutti i suoi figli appartengono alla classe TypedNameNode o TypedIntNameNode e rappresentano un nome semplice (senza pedice) o un int name (nome_intero) tipizzato.
    """
    def __init__(self, typedNames: list):
        super().__init__(typedNames)

        for typedName in typedNames:
            if not (isinstance(typedName, names.TypedNameNode) or isinstance(typedName, names.TypedIntNameNode)):
                raise TypeError(
                    f"typedNames deve essere una lista di TypedNameNode e TypedIntNameNode, non {type(typedName)}."
                )
        
        self.nodeName = "InductiveConstructParamsNode"


    def visit(self, interpreter):
        return super().visit(interpreter)


class AbstractConstructNode(tree.TreeNode):
    """
    Nodo astratto che rappresenta un construct salvandone i parametri richiesti, i valori
    di ritorno e i passi che esegue.
    La visita di questo nodo si limita a invocare lo stesso metodo visit sui suoi figli-step in ordine.
    """
    def __init__(self,
        constructName: str,
        stepsList: steps.StepsNode,
        params: AbstractConstructParamsNode,            # Un construct necessita sempre di input da cui partire
        results: AbstractConstructResultsNode = None    # Un construct può non restituire risultati
    ):
        
        if not isinstance(stepsList, steps.StepsNode):
            raise TypeError(f"stepsList deve essere di tipo StepsNode, non {type(stepsList)}.")
        if not isinstance(params, AbstractConstructParamsNode):
            raise TypeError(f"params deve essere di tipo AbstractConstructParamsNode, non {type(params)}.")
        if results and not isinstance(results, AbstractConstructResultsNode):
            raise TypeError(f"results deve essere di tipo AbstractConstructResultsNode, {type(results)}.")
        
        constructName = str(constructName)
        if len(constructName) == 0:
            raise ValueError("constructName non può essere vuoto.")

        resultsChild = []
        if results:
            resultsChild = [results]

        super().__init__(resultsChild + [params, stepsList])
        
        self.nodeName = "AbstractConstructNode"
        self.constructName = constructName


    @property
    def resultsTree(self):
        if self.childrenNum == 3:
            return self.children[0]
        else:
            return None
    

    @property
    def resultsNum(self):
        if self.resultsTree:
            return self.resultsTree.childrenNum
        else:
            return 0


    @property
    def paramsTree(self):
        return self.children[-2]
    

    @property
    def paramsNum(self):
        return self.paramsTree.childrenNum


    @property
    def stepsTree(self):
        return self.children[-1]

    
    @abstractmethod
    def visit(self, interpreter):
        return self.stepsTree.visit(interpreter)


class BaseConstructNode(AbstractConstructNode):
    """
    Nodo che rappresenta un construct non induttivo.
    La sua implementazione si limita a fare alcuni controlli di tipo non fatti da AbstractConstructNode.
    """
    def __init__(self,
        constructName: str,
        steps: steps.StepsNode,
        params: BaseConstructParamsNode,
        results: BaseConstructResultsNode = None,
    ):
        
        if not isinstance(params, BaseConstructParamsNode):
            raise TypeError(f"params deve essere di tipo BaseConstructParamsNode, non {type(params)}.")
        if results and not isinstance(results, BaseConstructResultsNode):
            raise TypeError(f"results deve essere di tipo BaseConstructResultsNode, non {type(results)}.")
        
        super().__init__(constructName, steps, params, results)
        self.nodeName = "BaseConstructNode"
    

    def visit(self, interpreter):
        return super().visit(interpreter)

    
class InductiveConstructNode(AbstractConstructNode):
    """
    Nodo che rappresenta un construct induttivo e che di conseguanza richiede che venga restituito sempre
    almeno un risultato.
    """
    def __init__(self,
        constructName: str,
        steps: steps.StepsNode,
        params: InductiveConstructParamsNode,
        results: InductiveConstructResultsNode      # I construct induttivi devono sempre restituire un risultato
    ):
        
        if not isinstance(params, InductiveConstructParamsNode):
            raise TypeError(f"params deve essere di tipo InductiveConstructParamsNode, non {type(params)}.")
        if not isinstance(results, InductiveConstructResultsNode):
            raise TypeError(f"results deve essere di tipo InductiveConstructResultsNode, non {type(results)}.")
        
        super().__init__(constructName, steps, params, results)
        self.nodeName = "InductiveConstructNode"
    

    def visit(self, interpreter):
        return super().visit(interpreter)
    