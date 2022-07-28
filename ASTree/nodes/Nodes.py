import Interpreter

from ASTree.nodes.TreeNode import *
from ASTree.nodes.NameNodes import *
from ASTree.nodes.EnteExpressionNodes import *
from ASTree.nodes.ConstructNodes import *
from ASTree.nodes.ConditionNodes import *
from ASTree.nodes.IntExpressionNodes import *
from ASTree.nodes.ExpressionNodes import *
from ASTree.nodes.StepNodes import *

import random
from typing import List
import geometry


class Ast(exprs.ListNode):
    """
    Nodo radice dell'AST su cui invocare il metodo di visita per l'interpretazione
    del codice a partire dal construct main. Gli input del programma sono ricavati dall'interprete
    passato in input al metodo visit o, se non sufficienti, generati casualmente tramite il metodo
    __generateRandomInput.
    I figli di questo nodo sono i nodi radice di tutti alberi relativi a construct sia induttivi sia non.
    """
    def __init__(
        self,
        constructs: List[AbstractConstructNode],
        approximate: bool = False
    ):
    
        super().__init__(constructs)

        for construct in constructs:
            if not isinstance(construct, AbstractConstructNode):
                raise TypeError(f"constructs deve essere una lista di AbstractConstructNode, non {type(construct)}.")
        
        self.nodeName = "AST"

        # Se True applica un'approssimazione nel calcolo delle intersezioni:
        self.approximate = bool(approximate)

        # Valori minimi e massimi delle coordinate di eventuali input generati casualmente:
        self.__minX = 0
        self.__maxX = 100
        self.__minY = 0
        self.__maxY = 100

    
    def visit(self, interpreter):
        if not isinstance(interpreter, Interpreter.Interpreter):
            raise TypeError(f"interpreter deve essere un oggetto di tipo Interpreter, non {type(interpreter).__name__}.")

        # Imposta l'approssimazione delle intersezioni:
        last_APPROXIMATE_INTERSECTIONS = geometry.APPROXIMATE_INTERSECTIONS
        geometry.APPROXIMATE_INTERSECTIONS = self.approximate

        # Salva il nodo radice di ogni construct nella memoria constructTable dell'interprete
        # indicando per ognuno se induttivo o non:
        for construct in self.children:
            if isinstance(construct, BaseConstructNode):
                constructType = "baseConstruct"
            else:
                constructType = "inductiveConstruct"

            # Salva i nodi radice dei constructs in una memoria dei constructs:
            interpreter.constructsTable.setValue(
                construct.constructName,
                construct,
                constructType,
                override = False    # Eventuali construct con uno stesso nome sollevano un errore
            )
        
        # Controllo che vi sia un construct main e che non sia induttivo:
        main, mainType = interpreter.constructsTable.getValue("main")
        if not main:
            raise NameError("Construct main non definito.")
        if mainType == "inductiveConstruct":
            raise TypeError("Il construct main non può essere definito come induttivo.")

        # Se il numero di input è maggiore di quelli richiesti solleva un'eccezione:
        if len(interpreter.inputs) > main.paramsNum:
            raise TypeError(
                f"Il construct main accetta {main.paramsNum} argomenti in input, non {len(interpreter.inputs)}."
            )
        
        # Genera la lista di input a partire da quelli passati all'interprete.
        # Se gli input sono minori di quelli richiesti i restanti vengono generati casualmente.       
        inputs = []        
        for i in range(main.paramsNum):
            param = main.paramsTree.children[i]

            # Se l'input non è presente viene generato casualmente:
            if i >= len(interpreter.inputs):
                interpreter.inputs.append(self.__generateRandomInput(interpreter, main, i))

            # Genera l'ente geometrico a partire dall'input i-esimo:
            try:
                if param.type == "point":
                    paramValue = geometry.Point(interpreter.inputs[i])
                else:   # line, ray, segment, circle:
                    paramValue = geometry.make_entity(
                        param.type,
                        geometry.Point(*interpreter.inputs[i][0]),
                        geometry.Point(*interpreter.inputs[i][1])
                    )
            except:
                raise TypeError(
                    f"main - Argomento {interpreter.inputs[i]} ({type(interpreter.inputs[i]).__name__}) non valido come parametro {param.nameTree.baseSymbol} di tipo {param.type}."
                )
            # Sostituisco nella lista inputs dell'interprete l'input tupla con il corrispondente
            # ente geometrico per una visualizzazione dell'output migliore:
            interpreter.inputs[i] = paramValue

            paramSymbol = param.nameTree.symbol(interpreter)
            # Salvo l'input in memoria:
            interpreter.actRecord.setValue(paramSymbol, paramValue, param.type)
            # Salvo il nome dell'input nella lista inputs:
            inputs.append(names.NameNode(paramSymbol))
            
        # InvocationNode di supporto per l'invocazione del construct main:
        results = entes.InvocationNode("main", inputs).visit(interpreter)

        # Ristabilisce il valore precedente di geometry.APPROXIMATE_INTERSECTIONS:
        geometry.APPROXIMATE_INTERSECTIONS = last_APPROXIMATE_INTERSECTIONS

        # Restituisce sempre una lista di risultati:
        if main.resultsNum == 1:
            return [results]
        else:
            return results


    def setRandomInputRange(
        self,
        minX: int = 0,
        maxX: int = 100,
        minY: int = 0,
        maxY: int = 100
    ):
        """
        Imposta il range in cui vengono generati eventuali input casuali.    
        """
        if not (isinstance(minX, int) and isinstance(maxX, int) and isinstance(minY, int) and isinstance(maxY, int)):
            raise TypeError("minX, maxX, minY e maxY devono essere valori interi.")
        self.__minX = minX
        self.__maxX = maxX
        self.__minY = minY
        self.__maxY = maxY
        
        # Un range vuoto non è accettabile:
        if self.__minX == self.__maxX:
            raise ValueError("minX e maxX non possono essere uguali.")
        if self.__minY == self.__maxY:
            raise ValueError("minY e maxY non possono essere uguali.")
        
        # Se il valore minimo è maggiore del massimo li scambia:
        if self.__minX > self.__maxX:
            self.__minX, self.__maxX = self.__maxX, self.__minX
        if self.__minY > self.__maxY:
            self.__minY, self.__maxY = self.__maxY, self.__minY        


    def __generateRandomInput(self, interpreter, main, i):
        """
        Genera l'input i-esimo in modo casuale e lo restituisce.
        Se l'input i-esimo deve essere un punto si assicura che esso non sia allineato a nessun altro
        punto in input, altrimenti che la retta individuata dai due punti dell'input non sia né parallela
        né perpendicolare alle altre.
        """
        param = main.paramsTree.children[i]
        
        if param.type == "point":
            while True:
                # Punto casuale:
                randomInput = (random.randint(self.__minX, self.__maxX), random.randint(self.__minY, self.__maxY))
                
                ok = True
                # Confronta il punto con gli altri punti in input precedenti:
                for j in range(i):
                    if main.paramsTree.children[j].type == "point":
                        # Se i punti sono allineati genera un nuovo punto:
                        if interpreter.inputs[j][0] == randomInput[0] or interpreter.inputs[j][1] == randomInput[1]:
                            ok = False
                            break
                
                # Se non vi sono punti allineati con quello generato lo restituisce, altrimenti resta nel ciclo while:
                if ok:
                    return randomInput

        else:   # line, ray, segment, circle
            while True:
                # Coppia di due punti casuali:
                randomInput = (
                    (random.randint(self.__minX, self.__maxX), random.randint(self.__minY, self.__maxY)),
                    (random.randint(self.__minX, self.__maxX), random.randint(self.__minY, self.__maxY))
                )

                # Se i due punti generati sono uguali continua:
                if randomInput[0] == randomInput[1]:
                    continue

                # Coefficiente angolare della retta per i due punti:
                if randomInput[0][0] - randomInput[1][0] == 0:
                    mRandom = 0
                else:
                    mRandom = (randomInput[0][1] - randomInput[1][1]) / (randomInput[0][0] - randomInput[1][0])

                ok = True
                # Confronta la retta individuata dai due punti con gli input precedenti:
                for j in range(i):
                    if main.paramsTree.children[j].type != "point":
                        # Coefficiente angolare della retta per i due punti dell'input j-esimo:
                        paramPoints = interpreter.inputs[j].points
                        if paramPoints[0][0] - paramPoints[1][0] == 0:
                            mParam = 0
                        else:
                            mParam = ((paramPoints[0][1] - paramPoints[1][1]) /
                                    (paramPoints[0][0] - paramPoints[1][0]))

                        # Accetta l'input solo se non parallelo o perpendicolare ad altre rette:
                        if mRandom == mParam or mRandom * mParam == - 1:
                            ok = False
                            break
                
                # Restituisce l'input se accettato, se no resta nel ciclo while:
                if ok:
                    return randomInput
