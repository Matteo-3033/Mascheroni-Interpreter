from numpy import interp
import ASTree.nodes.NameNodes as names
import ASTree.nodes.InductiveConstruct as ic
import ASTree.nodes.ExpressionNodes as exprs
import ASTree.nodes.TreeNode as tree

import geometry
from typing import List


class PrimitiveNode(exprs.EnteExpressionNode):
    """
    Nodo che rappresenta espressioni primitive nella forma <tipo>[Point, Point],
    con <tipo> uno tra "segment", "ray", "line", "circle".
    """

    def __init__(
        self,
        primitiveType: str,
        lhsEnteExpression: exprs.EnteExpressionNode,
        rhsEnteExpression: exprs.EnteExpressionNode
    ):

        if primitiveType not in {"segment", "ray", "line", "circle"}:
            raise ValueError(
                f'Tipo {primitiveType} non valido.\nPossibili valori: "line", "ray", "segment", "circle"'
            )

        if not isinstance(lhsEnteExpression, exprs.EnteExpressionNode):
            raise TypeError(f"lhsEnteExpression deve essere di tipo EnteExpressionNode, non {type(lhsEnteExpression)}.")
        if not isinstance(rhsEnteExpression, exprs.EnteExpressionNode):
            raise TypeError(f"rhsEnteExpression deve essere di tipo EnteExpressionNode, non {type(rhsEnteExpression)}.")

        super().__init__([lhsEnteExpression, rhsEnteExpression])
        self.primitiveType = primitiveType
        self.nodeName = "PrimitiveNode"


    @property
    def lhsParamTree(self):
        return self.children[0]

    
    @property
    def rhsParamTree(self):
        return self.children[1]


    def visit(self, interpreter):
        # Calcolo degli argomenti della primitiva
        left = self.lhsParamTree.visit(interpreter)
        right = self.rhsParamTree.visit(interpreter)

        # Gli IntersectionNode e gli InvocationNode potrebbero restituire più di un risultato sotto forma di lista:
        if isinstance(left, list):
            raise ValueError(f"La valutazione del primo argomento della primitiva \"{self.primitiveType}\" restituisce più di un'entità, ({len(left)}).")
        if isinstance(right, list):
            raise ValueError(f"La valutazione del secondo argomento della primitiva \"{self.primitiveType}\" restituisce più di un'entità ({len(right)}).")
        
        # (valore, tipo)
        leftValue, leftType = left
        rightValue, rightType = right

        if leftType != "point" or rightType != "point":
            raise TypeError(
                f"Gli argomenti di una primitiva devono essere due point, non {leftType} e {rightType}:\n{self.primitiveType}[{leftValue}, {rightValue}]"
            )
        if leftValue == rightValue:
            raise ValueError(
                f"Gli argomenti di una primitiva devono essere due point distinti:\n{self.primitiveType}[{leftValue}, {rightValue}]"
            )
        
        # Creazione dell'ente geometrico indicato da self.primitiveType
        return geometry.make_entity(self.primitiveType, leftValue, rightValue), self.primitiveType


class IntersectionNode(exprs.BinaryOperatorNode, exprs.EnteExpressionNode):
    """
    Nodo che rappresenta operazioni di intersezione tra enti geometrici non di tipo point.
    """
    def __init__(
        self,
        op: str,
        lhsEnteExpression: exprs.EnteExpressionNode,
        rhsEnteExpression: exprs.EnteExpressionNode
    ):
    
        if op not in {"^", "^0", "^1"}:
            raise ValueError(
                f'Operatore {op} non valido.\nPossibili operatori:\n"∩", "∩0", "∩1"'
            )

        if not isinstance(lhsEnteExpression, exprs.EnteExpressionNode):
            raise TypeError(f"lhsEnteExpression deve essere di tipo EnteExpressionNode, non {type(lhsEnteExpression)}.")
        if not isinstance(rhsEnteExpression, exprs.EnteExpressionNode):
            raise TypeError(f"rhsEnteExpression deve essere di tipo EnteExpressionNode, non {type(rhsEnteExpression)}.")

        super().__init__(op, lhsEnteExpression, rhsEnteExpression)
        self.nodeName = "IntersectionNode"


    def visit(self, interpreter):
        # Calcolo degli enti geometrici su cui eseguire l'intersezione:
        left = self.lhsExpressionTree.visit(interpreter)
        right = self.rhsExpressionTree.visit(interpreter)

        # Gli IntersectionNode e gli InvocationNode potrebbero restituire più di un risultato:
        if isinstance(left, list):
            raise ValueError(f"La valutazione del primo argomento dell'intersezione restituisce più di un'entità, ({len(left)}).")
        if isinstance(right, list):
            raise ValueError(f"La valutazione del secondo argomento dell'intersezione restituisce più di un'entità ({len(right)}).")
        
        leftValue, leftType = left
        rightValue, rightType = right

        if leftType not in interpreter.GEOMETRY_TYPES - {"point"} or rightType not in interpreter.GEOMETRY_TYPES - {"point"}:
            raise RuntimeError(
                f"È possibile calcolare l'intersezione solamente di enti geometrici che non siano point, non tra {leftType} e {rightType}:\n{leftValue} {self.op} {rightValue}"
            )
        
        # Applicazione dell'operatore di intersezione sui operandi:
        try:
            res = interpreter.opDT[self.op](leftValue, rightValue, approx = geometry.APPROXIMATE_INTERSECTIONS)
        except BaseException as e:
            raise RuntimeError(
                f"Invalido numero di intersezioni tra {leftValue} e {rightValue}; se l'input è stato generato casualmente l'errore potrebbe essere dovuto agli input generati."
            )
        
        # Se i risultati sono più di uno restituisce una lista, altrimenti il singolo risultato.
        if isinstance(res, tuple):  # Più di un risultato
            return [(point, "point") for point in res]
        else:   # Un solo risultato
            return res, "point"


class InvocationNode(exprs.EnteExpressionNode):
    """
    Nodo che rappresenta invocazioni di un construct di cui salva il nome e la lista di
    parametri. Il metodo di visita di questo nodo agisce diversamente a seconda che il
    construct sia induttivo o non:
    - Se è induttivo restituisce un oggetto della classe InductiveConstruct per ogni risultato definito
        dal construct;
    - Se non è induttivo valuta il construct per i parametri passati e ne restituisce i risultati.
    """
    def __init__(
        self,
        constructName: str,
        params: List[exprs.EnteExpressionNode]
    ):

        constructName = str(constructName)
        if len(constructName) == 0:
            raise ValueError("constructName non può essere vuoto")

        if not isinstance(params, list):
            raise TypeError("params deve essere una lista di EnteExpressionNode.")
        for param in params:
            if not isinstance(param, exprs.EnteExpressionNode):
                raise TypeError(f"param deve essere di tipo EnteExpressionNode, non {type(param)}.")
        
        super().__init__(params)
        self.constructName = constructName
        self.nodeName = "InvocationNode"


    def visit(self, interpreter):
        # Nodo radice del construct da invocare:
        constructTree, constructType = interpreter.constructsTable.getValue(self.constructName)
        if not constructTree:
            raise NameError(f"Construct {self.constructName} non definito.")
        
        # Controlo che il construct invocato non sia già attivo per evitare casi di ricorsione:
        if self.constructName in interpreter.activeConstructs:
            raise RecursionError(
                f"Invocazione del construct già attivo {self.constructName}: la ricorsione non è supportata dal linguaggio."
            )

        # Controllo sul numero di parametri:
        if constructTree.paramsNum != self.childrenNum:
            raise TypeError(
                f"Il construct {self.constructName} accetta {constructTree.paramsNum} argomenti in input, non {self.childrenNum}."
            )
                
        # Lista dei parametri:
        params = []
        for i in range(constructTree.paramsNum):
            # Parametro definito dal construct:
            constructParam = constructTree.paramsTree.children[i]
            # Argomento passato in input al construct
            param = self.children[i].visit(interpreter)
            
            # IntersectionNodes e InvocationNodes potrebbe restituire più risultati:
            if isinstance(param, list):
                raise TypeError(f"La valutazione del {i + 1}° argomento del construct {self.constructName} restituisce più di un'entità ({len(param)}).")

            # param è una tupla (valore, tipo):
            paramValue, paramType = param

            # Controllo sui tipi:
            if paramType != constructParam.type:
                raise TypeError(
                    f"Argomento {paramValue} di tipo \"{paramType}\" non valido come parametro {constructParam.nameTree.symbol(interpreter)} di tipo \"{constructParam.type}\" del construct {self.constructName}."
                )

            # simbolo, valore, tipo:
            params.append((constructParam.nameTree.symbol(interpreter), paramValue, paramType))

        # Se il construct è induttivo ci si limita a creare un oggetto di tipo InductiveConstruct
        # per ogni risultato definito dal construct e a restituirli:
        if constructType == "inductiveConstruct":
            # Lista di oggetti inductiveConstruct, uno per ogni risultato del construct:
            results = []
            for i in range(constructTree.resultsNum):
                result = ic.InductiveConstruct(constructTree, params, whichOne = i)
                results.append((result, result.resultType))

            # Per ogni construct si salva un riferimento agli altri:
            for i in range(len(results)):
                results[i][0].setResults([results[j][0] for j in range(len(results)) if j != i])
            
            # Un unico risultato è restituito singolarmente, più di uno come lista:
            if len(results) == 1:
                return results[0]
            else:
                return results
        
        
        # Se il construct non è induttivo viene eseguito:
        
        # Attivazione del record di attivazione del construct:
        interpreter.newActRecord()
        
        # Salvataggio del nome del nuovo construct corrente:
        parentConstructName = interpreter.currentConstructName
        interpreter.currentConstructName = self.constructName
        
        # Segna il construct come attivo:
        interpreter.activeConstructs.add(self.constructName)

        # Salvataggio nel nuovo record di attivazione dei parametri:
        for symbol, value, symbolType in params:
            interpreter.actRecord.setValue(symbol, value, symbolType)
        
        # Esecuzione del construct:
        constructTree.visit(interpreter)
        
        # Lista dei risultati:
        results = []
        for i in range(constructTree.resultsNum):
            constructResult = constructTree.resultsTree.children[i]

            # Valore e tipo del risultato i-esimo:
            resultValue, resultType = interpreter.actRecord.getValue(constructResult.nameTree.symbol(interpreter))

            if not resultValue:
                raise NameError(f"Valore di ritorno {constructResult.nameTree.symbol(interpreter)} non definito.")

            # Controllo del tipo del risultato:
            if resultType != constructResult.type:
                raise TypeError(
                    f"Tipo del valore di ritorno {constructResult.nameTree.symbol(interpreter)} ({resultType}) diverso da quello restituito ({constructResult.type})."
                )
            elif isinstance(resultValue, ic.InductiveConstruct):
                raise TypeError(
                    f"Tipo induttivo del valore di ritorno {constructResult.nameTree.symbol(interpreter)} non ammesso per il risultato di tipo dichiarato {constructResult.type}."
                )

            results.append((resultValue, resultType))

        
        # Ripristino del nome dell'ultimo construct attivo:
        interpreter.currentConstructName = parentConstructName

        # Segna il construct come non attivo:
        interpreter.activeConstructs.remove(self.constructName)

        # Ripristino del precedente record di attivazione:
        interpreter.discardActRecord()
        
        # Un unico risultato è restituito singolarmente, più di uno come lista:
        if len(results) == 1:
            return results[0]
        else:
            return results


class UpToNamedExpressionNode(tree.TreeNode):
    """
    Nodo che associa una lista di nomi a un'espressione sugli enti i cui risultati devono essere
    assegnati a tali nomi. Se è definito un valore upTo i risultati dell'espressione deve corrispondere
    a un ente induttivo.
    """
    def __init__(
        self,
        enteExpression: exprs.EnteExpressionNode,
        namesList: names.NamesNode,
        upTo: exprs.IntExpressionNode = None
    ):

        if not isinstance(enteExpression, exprs.EnteExpressionNode):
            raise TypeError(f"enteExpressione deve essere di tipo EnteExpressionNode, non {type(enteExpression)}.")
        if not isinstance(namesList, names.NamesNode):
            raise TypeError(f"namesList deve essere di tipo InductiveNamesNode, non {type(namesList)}.")
        if upTo and not isinstance(upTo, exprs.IntExpressionNode):
            raise TypeError(f"upTo deve essere di tipo IntExpressionNode, non {type(upTo)}.")
        
        if upTo:
            for name in namesList.children:
                # Non sono ammesse definizioni upto se il nome non è semplice (se ha un pedice):
                if not isinstance(name, names.NameNode):
                    raise ValueError(
                        "I costruct induttivi utilizzati in una definizione con clausola upto devono essere associati a un nome semplice."
                    )

        upToChild = []
        if upTo:
            upToChild = [upTo]
        
        super().__init__([enteExpression, namesList] + upToChild)
        self.nodeName = "UpToNamedExpressionNode"

    
    @property
    def expressionTree(self):
        return self.children[0]


    @property
    def namesTree(self):
        return self.children[1]
    

    @property
    def upToTree(self):
        if self.childrenNum > 2:
            return self.children[-1]
        else:
            return None

    
    def visit(self, interpreter):
        results  = self.expressionTree.visit(interpreter)

        if not results:
            raise ValueError(
                f"Nessun valore di ritorno da assegnare a {', '.join([name.symbol(interpreter) for name in self.namesTree.children])}."
            )

        # Un risultato unico è una tupla (valore, tipo), mentre risultati multipli una lista di tuple.
        if isinstance(results, tuple):
            results = [results]

        # Controllo che il numero di risultati sia pari al numero di nomi dichiarati.
        if len(results) != self.namesTree.childrenNum:
            raise ValueError(
                f"{len(results)} enti restituiti, ma {self.namesTree.childrenNum} nomi dichiarati: {', '.join([name.symbol(interpreter) for name in self.namesTree.children])}.\nSe l'input è generato in modo casuale l'errore potrebbe essere dovuto ai punti generati."
            )
        
        # Associa in memoria ogni risultato a un nome:
        for i in range(len(results)):
            if results[i][1] not in interpreter.GEOMETRY_TYPES:
                raise TypeError(f"È possibile definire solamente enti geometrici, non {results[i][1]}.")
            interpreter.actRecord.setValue(
                self.namesTree.children[i].symbol(interpreter),
                *results[i]
            )
        
        # Se è presenta una clausola upto definisce i nomi per n da 0 a upto compreso:
        if self.upToTree:
            # Valore di upTo:
            upTo, upToType = self.upToTree.visit(interpreter)

            if upToType != "int":
                raise TypeError(f"Il valore di upto deve essere intero, non {upToType}.")
            if upTo < 0:
                raise ValueError(f"Il valore di upto deve essere un intero positivo, non {upTo}.")
            
            for name in self.namesTree.children:
                # Simbolo induttivo:
                symbol = name.symbol(interpreter)

                # Il risultato dell'operazione deve essere un oggetto InductiveConstruct per applicare la clausola upto:
                value, _ = interpreter.actRecord.getValue(symbol)
                if not isinstance(value, ic.InductiveConstruct):
                    raise TypeError(f"Non è possibile eseguire una definizione upto su un ente non induttivo, {value}.")
                elif value.currentLevel and upTo >= value.currentLevel:
                    raise RecursionError(
                        "I construct induttivi possono essere definiti solamente in funzione di enti di livello inferiore del corrente."
                    )

                # Definisce tutti gli enti per n da 0 a upTo compreso:
                for n in range(upTo + 1):
                    interpreter.actRecord.setValue(
                        f"{symbol}_{n}",
                        *value(interpreter, n)  # Calcolo del construct per n, restituisce (valore, tipo)
                    )


class NamedExpressionNode(UpToNamedExpressionNode):
    """
    Nodo che associa una lista di nomi a un'espressione sugli enti i cui risultati devono essere
    assegnati a tali nomi.
    """
    def __init__(
        self,
        enteExpression: exprs.EnteExpressionNode,
        namesList: names.NamesNode
    ):
        
        super().__init__(enteExpression, namesList)
        self.nodeName = "NamedExpressionNode"

    
    def visit(self, interpreter):
        return super().visit(interpreter)



class NamedExpressionsNode(exprs.ListNode):
    """
    Nodo che ha solamente figli di tipo NamedExpressionNode.
    """
    def __init__(
        self,
        namedExpressions: List[UpToNamedExpressionNode]
    ):

        super().__init__(namedExpressions)
        
        for namedExpression in namedExpressions:
            if not isinstance(namedExpression, UpToNamedExpressionNode):
                raise TypeError(
                    f"namedExpressions deve essere una lista di UpToNamedExpressionNode, non {type(namedExpression)}."
                )

        self.nodeName = "NamedExpressionsNode"


    def visit(self, interpreter):
        return super().visit(interpreter)
