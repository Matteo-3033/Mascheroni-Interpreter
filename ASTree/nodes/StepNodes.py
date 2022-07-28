import ASTree.nodes.EnteExpressionNodes as entes
import ASTree.nodes.InductiveConstruct as ic
import ASTree.nodes.ExpressionNodes as exprs
import ASTree.nodes.TreeNode as tree
import ASTree.nodes.NameNodes as names

from typing import List
import geometry


class StepNode(tree.TreeNode):
    """
    Nodo astratto che rappresenta un passo d'esecuzione all'interno di un construct.
    """
    def __init__(
        self,
        children: list = list()
    ):
        super().__init__(children)
        self.nodeName = "StepNode"


class StepsNode(exprs.ListNode):
    """
    Nodo i cui figli sono tutti di tipo StepNode.
    """
    def __init__(
        self,
        steps: List[StepNode]
    ):
        super().__init__(steps)

        for step in steps:
            if not isinstance(step, StepNode):
                raise TypeError(f"steps deve essere una lista di StepNode, non {type(step)}.")

        self.nodeName = "StepsNode"


    def visit(self, interpreter):
        return super().visit(interpreter)


class DrawLabelNode(StepNode):
    """
    Nodo che rappresenta un'operazione di showLabel.
    """
    def __init__(self):
        super().__init__()
        self.showLabel = True
        self.nodeName = "DrawLabelNode"


    def visit(self, interpreter):
        # Dizionario di coppie nome - entità geometrica:
        entitiesDict = {name: value[0]
            for name, value in interpreter.actRecord.toDict().items()   # Gli items sono tuple (simbolo, (valore, tipo))
            if value[1] in interpreter.GEOMETRY_TYPES
        }
        
        # Nodo radice del construct corrente:
        constructTree, _ = interpreter.constructsTable.getValue(interpreter.currentConstructName)
        
        # Nomi dei parametri del construct corrente:
        params = set()
        for param in constructTree.paramsTree.children:
            params.add(param.nameTree.symbol(interpreter))
        
        # Nomi dei risultati del costruct corrente:
        results = set()
        if constructTree.resultsTree:
            for result in constructTree.resultsTree.children:
                results.add(result.nameTree.symbol(interpreter))
        
        # Passa all'interprete il risultato per la visualizzazione:
        svg = geometry.to_svg(
            entitiesDict,
            params,
            results,
            self.showLabel
        )
        
        if svg is None:
            raise RuntimeError("Errore di visualizzazione.")
        
        interpreter.show(svg)


class DrawNode(DrawLabelNode):
    """
    Nodo che rappresenta un'operazione di show.
    """
    def __init__(self):
    
        super().__init__()
        self.showLabel = False
        self.nodeName = "DrawNode"


    def visit(self, interpreter):
        return super().visit(interpreter)
        

class AssignementNode(StepNode):
    """
    Nodo che rappresenta un'operazione di assegnamento di un valore intero a un simbolo in memoria.
    """
    def __init__(
        self,
        name: names.NameNode,
        intExpression: exprs.IntExpressionNode
    ):

        if not isinstance(name, names.NameNode):
            raise TypeError(f"name deve essere di tipo NameNode, non {type(name)}.")
        if not isinstance(intExpression, exprs.IntExpressionNode):
            raise TypeError(f"intExpression deve essere di tipo IntExpressionNode, non {type(intExpression)}.")
        
        super().__init__([name, intExpression])
        self.nodeName = "AssignementNode"


    @property
    def nameTree(self):
        return self.children[0]
    

    @property
    def expressionTree(self):
        return self.children[1]


    def visit(self, interpreter):
        # Simbolo a cui assegnare il valore dell'espressione intera:
        name = self.nameTree.symbol(interpreter)

        if interpreter.actRecord.getValue(name)[1] in interpreter.GEOMETRY_TYPES:
            raise NameError(
                f"Simbolo {name} già definito come nome di un ente geometrico, impossibile eseguire un riassegnamento."
            )
        
        # Valutazione dell'espressione intera:
        value, valueType = self.expressionTree.visit(interpreter)
        if valueType != "int":
            raise TypeError(
                f"È possibile eseguire assegnamenti solamente di interi, non {valueType}:\nlet {name} = {value}"
            )
        
        # Se al simbolo è già associato un valore valore intero questo viene sovrascritto.
        # Se la sovrascrittura avviene in un sub-scope rispetto a quello in cui il simbolo è stato definito
        # per la prima volta questa viene mantenuta anche dopo l'uscita dal sub-scope.
        interpreter.actRecord.setValue(
            name,
            value,
            valueType,
            override = True     # Il riassegnamento di espressioni intere è permesso
        )


class WithNode(StepNode):
    """
    Nodo che definisce un nuovo sub-scope in cui eseguire i passi in esso contenuti.
    """
    def __init__(
        self,
        defines: entes.NamedExpressionsNode,
        steps: StepsNode
    ):
        
        if not isinstance(defines, entes.NamedExpressionsNode):
            raise TypeError(f"defines deve essere di tipo NamedExpressionsNode, non {type(defines)}.")
        if not isinstance(steps, StepsNode):
            raise TypeError(f"steps deve essere di tipo StepsNode, non {type(steps)}.")
        
        super().__init__([defines, steps])
        self.nodeName = "WithNode"


    @property
    def definesTree(self):
        return self.children[0]
    

    @property
    def stepsTree(self):
        return self.children[-1]


    def visit(self, interpreter):
        interpreter.enterScope()
        self.definesTree.visit(interpreter)
        self.stepsTree.visit(interpreter)
        interpreter.exitScope()


class IfThenElseNode(StepNode):
    """
    Nodo che rappresenta un blocco if-then-else di cui salva la condizione e i blocchi
    "true" e "false".
    """
    def __init__(
        self,
        condition: exprs.ConditionNode,
        trueSteps: StepsNode,
        falseSteps: StepsNode = None
    ):
    
        if not isinstance(condition, exprs.ConditionNode):
            raise TypeError(f"condition deve essere di tipo ConditionNode, non {type(condition)}.")
        if not isinstance(trueSteps, StepsNode):
            raise TypeError(f"trueSteps deve essere di tipo StepsNode, non {type(trueSteps)}.")
        if falseSteps and not isinstance(falseSteps, StepsNode):
            raise TypeError(f"falseSteps deve essere di tipo StepsNode, non {type(falseSteps)}.")

        falseStepsChild = []
        if falseSteps:
            falseStepsChild = [falseSteps]

        super().__init__([condition, trueSteps] + falseStepsChild)
        self.nodeName = "IfThenElseNode"


    @property
    def conditionTree(self):
        return self.children[0]


    @property
    def TrueTree(self):
        return self.children[1]


    @property
    def FalseTree(self):
        if self.childrenNum > 2:
            return self.children[2]
        else:
            return None


    def visit(self, interpreter):
        # Valuta la condizione e a seconda del suo valore visita
        # il blocco true o il blocco false:
        if self.conditionTree.visit(interpreter)[0]:
            interpreter.enterScope()
            self.TrueTree.visit(interpreter)
            interpreter.exitScope()

        elif self.FalseTree:    # Condizione falsa
            interpreter.enterScope()
            self.FalseTree.visit(interpreter)
            interpreter.exitScope()


class IfThenNode(IfThenElseNode):
    """
    Nodo if-then.
    """
    def __init__(
        self,
        condition: exprs.ConditionNode,
        trueSteps: StepsNode
    ):

        super().__init__(condition, trueSteps)
        self.nodeName = "IfThenNode"


    def visit(self, interpreter):
        return super().visit(interpreter)


class DefineNode(StepNode):
    """
    Nodo che rappresenta un'operazione di define di un ente induttivo.
    """
    def __init__(
        self,
        namedExpression: entes.UpToNamedExpressionNode
    ):
        
        if not isinstance(namedExpression, entes.UpToNamedExpressionNode):
            raise TypeError(f"namedExpression deve essere di tipo UpToNamedExpressionNode, non {type(namedExpression)}.")
        
        super().__init__([namedExpression])
        self.nodeName = "DefineNode"
        

    @property
    def expressionTree(self):
        return self.children[0]


    def visit(self, interpreter):
        # La valutazione del nodo UpToNamedExpressionNode associa i valori
        # restituiti da un'espressione sugli enti ad altrettanti nomi:
        self.expressionTree.visit(interpreter)

        # Salva i nomi definiti dall'espressione come permanenti nel record di attivazione
        # in modo che all'uscita da un sub-scope vengano mantenuti in memoria:
        for name in self.expressionTree.namesTree.children:
            interpreter.actRecord.defineSymbol(name.symbol(interpreter))

        # Se è presenta una clausola upto salva come permanenti anche i valori definiti
        # in questo modo:
        if self.expressionTree.upToTree:
            # Valore di upTo:
            upTo, _ = self.expressionTree.upToTree.visit(interpreter)

            for name in self.expressionTree.namesTree.children:
                for n in range(upTo + 1):
                    interpreter.actRecord.defineSymbol(f"{name.symbol(interpreter)}_{n}")
           
        