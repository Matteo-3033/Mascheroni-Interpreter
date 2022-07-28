import ASTree.nodes.TreeNode as tree

import geometry
from typing import List, Tuple, Type


class InductiveConstruct:
    """
    Classe di supporto per i construct induttivi che salva il nodo radice dell'albero del
    construct e la lista dei suoi parametri e restituisce il risultato passato come valore whichOne al costruttore.
    Tramite l'operatore di call è possibile passando in input un intero n visitare l'albero ricorsivamente per eseguire l'induzione a partire da n.
    Nel caso il construct restituisca più di un risultato è necessario passare all'oggetto tramite il metodo setResults
    dei riferimenti ad altri oggetti di tipo InductiveConstruct definito per lo stesso construct, ma con valore whichOne
    diverso.
    """
    def __init__(
        self,
        constructTree: tree.TreeNode,
        params: List[Tuple[str, geometry.GeometryEntity, str]],     # lista di triple simbolo - valore - tipo
        whichOne: int = 0
    ):

        if not isinstance(constructTree, tree.TreeNode):
            raise TypeError(f"constructTree deve essere di tipo TreeNode, non {type(constructTree)}.")
        
        if not isinstance(params, list):
            raise TypeError("params deve essere una lista di triple (simbolo, valore, tipo).")
        if len(params) != constructTree.paramsTree.childrenNum:
            raise RuntimeError(
                f"Il construct {constructTree.constructName} accetta {constructTree.paramsTree.childrenNum} argomenti in input, non {len(params)}."
            )

        # Controllo sui parametri:
        for i in range(constructTree.paramsNum):
            if not isinstance(params[i], tuple) or len(params[i]) != 3:
                raise TypeError("Ogni elemento nella lista params deve essere una tupla (simbolo, valore, tipo).")
            
            param = constructTree.paramsTree.children[i]
            
            # Controllo sui tipi dei parametri:
            if params[i][2] != param.type:
                raise TypeError(
                    f"Argomento {param[i][1]} di tipo \"{param[i][2]}\" non valido come parametro {param[i][0]} di tipo \"{param.type}\" del construct {constructTree.constructName}."
                )
            

        if not isinstance(whichOne, int):
            raise TypeError("whichOne deve essere intero.")
        if not 0 <= whichOne < constructTree.resultsNum:
            raise ValueError(f"whichOne deve essere un intero positivo minore di {constructTree.resultsNum}, non {whichOne}.")
        
        self.__constructTree = constructTree                    # Nodo radice del construct
        self.__params = params                                  # Lista dei parametri
        self.__whichOne = whichOne                              # Indice del risultato da restituire
        self.__baseName = self.resultNameTree.baseSymbol        # Nome induttivo base (senza il pedice)

        # Lista di riferimenti ad altri oggetti InductiveConstruct che restituiscono risultati diversi
        self.__inductiveConstructs = {self.__whichOne: self}
        
        # True se in self.__inductiveConstructs è presente un riferimento per ogni risultato:
        self.__resultsSetted = False
        if constructTree.resultsNum == 1:
            self.__resultsSetted = True

        # Dizionario dei valori per n già calcolati, per evitare di doverli ricalcolare più volte.
        # Si utilizza un dizionario invece di una lista perché non è detto che la base induttiva parta da 0.
        self.__ns = dict()

        self.currentLevel = None                                # Livello di induzione corrente


    @property
    def resultNameTree(self):
        return self.__constructTree.resultsTree.children[self.__whichOne].nameTree


    @property
    def resultType(self):
        return self.__constructTree.resultsTree.children[self.__whichOne].type
    

    def setResults(self, inductiveConstructs: list = list()):
        """
        Metodo da invocare nel caso il construct induttivo restituisca più di
        un risultato passando nella lista inductiveConstructs gli oggetti di tipo
        inductiveConstruct con valore whichOne diverso da quello di questo oggetto.
        """
        if not isinstance(inductiveConstructs, list):
            raise TypeError("inductiveConstructs deve essere una lista.")
        
        for inductiveConstruct in inductiveConstructs:
            if not isinstance(inductiveConstruct, InductiveConstruct):
                raise TypeError(
                    f"inductiveConstructs deve essere una lista di InductiveConstruct, non {type(inductiveConstruct)}."
                )

            # Controlla che inductiveConstruct faccia riferimento allo stesso construct induttivo di self.
            # Il controllo è fatto in base al nome del construct perché non possono essere definiti due construct
            # con lo stesso nome.
            if inductiveConstruct.__constructTree.constructName != self.__constructTree.constructName:
                raise ValueError(
                    f"inductiveConstructs deve essere una lista di InductiveConstruct definiti sullo stesso construct induttivo dell'oggetto a cui è passata."
                )

            if inductiveConstruct.__whichOne != self.__whichOne:
                self.__inductiveConstructs[inductiveConstruct.__whichOne] = inductiveConstruct
            else:
                raise ValueError(f"Impossibile passare un nuovo oggetto per il risultato {self.__whichOne}.")
        
        # Controlla se c'è un riferimento per ogni risultato:
        self.__resultsSetted = True
        for i in range(self.__constructTree.resultsNum):
            if i not in self.__inductiveConstructs:
                self.__resultsSetted = False
                break


    def __call__(self, interpreter, n: int):
        """
        Metodo di call per eseguire il construct induttivo sul livello di induzione n.        
        """
        if not self.__resultsSetted:
            raise RuntimeError(
                "Riferimenti per i risultati mancanti.\nPrima di una invocare il metodo di call passare i riferimentri tramite il metodo setResults(list)."
            )

        # Il livello di induzione deve essere un intero positivo:
        if not isinstance(n, int):
            raise TypeError(f"n deve essere intero.")
        if n < 0:
            raise RuntimeError(
                f"Livello di induzione negativo {n} non ammesso.\nControllare che il pedice del nome induttivo non sia negativo e di aver definito correttamente la base dell'induzione."
            )
        n = int(n)
        
        if n in self.__ns.keys():
            return self.__ns[n], self.resultType

        # Simbolo con cui verrà salvato il risultato in memoria:
        resultSymbol = self.__baseName + '_' + str(n)

        # Attivazione del nuovo record di attivazione:
        interpreter.newActRecord()
        
        # Salvo il nome del construct corrente:
        parentConstructName = interpreter.currentConstructName
        interpreter.currentConstructName = self.__constructTree.constructName
        
        # Definizione dei parametri:
        for symbol, value, symbolType in self.__params:
            # Se il risultato richiesto è definito direttamente come parametro lo restituisce:
            if symbol == resultSymbol:
                if symbolType != self.resultType:
                    raise TypeError(
                        f"Tipo del valore di ritorno {resultSymbol} ({self.resultType}) diverso da quello del parametro {symbol} ({symbolType})."
                    )
                interpreter.discardActRecord()
                interpreter.currentConstructName = parentConstructName
                self.__ns[n] = value
                return value, symbolType
            
            # Altrimenti salva il parametro in memoria associato al suo simbolo:
            interpreter.actRecord.setValue(symbol, value, symbolType)
        
        # Salvo un riferimento a un oggetto inductiveConstruct per ogni risultato:
        for inductiveConstruct in self.__inductiveConstructs.values():
            interpreter.actRecord.setValue(inductiveConstruct.__baseName, inductiveConstruct, inductiveConstruct.resultType)

        # Salvo n in memoria:
        interpreter.actRecord.setValue(self.resultNameTree.rhsTree.baseSymbol, n, "int")
        lastLevel = self.currentLevel
        self.currentLevel = n
        
        # Aggiungo il construct all'insieme di quelli attivi:
        wasActive = True
        if self.__constructTree.constructName not in interpreter.activeConstructs:
            wasActive = False
            interpreter.activeConstructs.add(self.__constructTree.constructName)

        # Visito il construct con l'n specificato:
        self.__constructTree.visit(interpreter)

        # Risultato:
        resultValue, resultType = interpreter.actRecord.getValue(resultSymbol)
        
        if not resultValue:
            raise NameError(f"Valore di ritorno {resultSymbol} non definito.")
        
        # Controllo del tipo del risultato:
        if resultType != self.resultType:
            raise TypeError(
                f"Tipo del valore di ritorno {resultSymbol} ({resultType}) diverso da quello restituito ({resultType})."
            )

        # Ripristino del record di attivazione precedente:
        interpreter.discardActRecord()

        # Ripristino del nome del construct precedente:
        interpreter.currentConstructName = parentConstructName
        self.currentLevel = lastLevel

        # Rimuovo il construct dall'insieme di quelli attivi se alla prima invocazione
        # non era già attivo:
        if not wasActive:
            interpreter.activeConstructs.remove(self.__constructTree.constructName)
        
        # Salva il risultato tra quelli già calcolati per evitare di ricalcolarlo più volte:
        self.__ns[n] = resultValue

        return resultValue, resultType
    