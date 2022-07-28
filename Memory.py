from typing import Any


class Memory:
    """
    Memoria associativa che permette di associare un nome a oggetti di tipo geometrico o intero assieme al loro tipo
    e di accedervi in un secondo momento tramite il nome.
    
    L'operazione di bind può essere eseguita tramite il metodo setValue, mentre quella di look up tramite getValue;
    i metodi enterScope e exitScope restituiscono invece un oggetto di tipo Memory che rappresenta rispettivamente
    un nuovo sub-scope o quello di livello superiore. Il metodo defineSymbol permette invece di indicare come "defined"
    un simbolo salvato in memoria, in modo che all'uscita dallo scope in cui è definito venga comunque mantenuto.
    """

    def __init__(self, parent = None):
        if parent and not isinstance(parent, Memory):
            raise TypeError(f"Il parametro parent deve essere di tipo Memory, non {type(parent)}")

        self.__parent = parent               # Riferimento allo scope di livello superiore
        self.__symbols = dict()              # Dizionario simbolo - valore
        self.__definedSymbols = set()        # Insieme dei simboli "defined"            

    
    def getValue(self, symbol: str):
        """
        Restituisce il valore associato al simbolo symbol in memoria e il suo tipo.
        Se il simbolo non è presente in memoria restituisce (None, None).
        """
        if symbol in self.__symbols:
            return self.__symbols[symbol]
        if self.__parent:
            return self.__parent.getValue(symbol)
        return (None, None)
        

    def setValue(
        self,
        symbol: str,
        value: Any,
        valueType: str,
        override: bool = False
    ):
        """
        Associa al simbolo symbol il valore value e il tipo valueType in memoria.
        Se override è True e il simbolo è già definito in memoria, anche in uno scope
        di livello superiore, il suo valore viene sovrascritto, altrimenti viene
        sollevata un'eccezione.
        """
        if len(symbol) == 0:
            raise ValueError("symbol non può essere vuoto.")
        
        # Se override è False e il simbolo è già definito solleva un errore:
        if not override and self.getValue(symbol)[0] is not None:
            raise NameError(f"Simbolo {symbol} già definito.")
        
        # Se override è True e il simbolo è presente in uno scope di livello
        # superiore ne modifica direttamente il valore:
        if override and self.__parent and self.__parent.getValue(symbol)[0] is not None:
            self.__parent.setValue(symbol, value, valueType, override)
        else:  # Altrimenti lo definisce nello scope corrente
            self.__symbols[symbol] = (value, valueType)

    
    def defineSymbol(self, symbol: str):
        """
        Definisce un simbolo a cui è già associato un valore in memoria in
        modo che venga mantenuto anche dopo l'uscita dallo scope in cui
        è stato definito per la prima volta.
        """
        if self.getValue(symbol)[0] is None:
            raise NameError(f"Simbolo \"{symbol}\" non definito.")
        self.__definedSymbols.add(symbol)


    def deleteValue(self, symbol: str):
        """
        Elimina le informazioni associate a symbol in memoria.
        Se symbol non è definito in memoria non fa nulla.
        """
        if symbol in self._symbols:
            self.__symbols.pop(symbol)
            self.__definedSymbols.discard(symbol)
        elif self.__parent:
            self.__parent.deleteValue(symbol)


    def enterScope(self):
        """
        Esegue un'operazione di enter in un nuovo scope dallo scope corrente e restituisce un oggetto
        di tipo Memory che rappresenta il nuovo scope.
        """
        return Memory(self)


    def exitScope(self):
        """
        Esegue un'operazione di exit dallo scope corrente e restituisce un oggetto di tipo Memory
        che rappresenta lo scope ripristinato.
        """
        if self.__parent is None:
            raise MemoryError("Nessuno scope da cui uscire; definirne prima uno tramite il metodo enter().")

        for symbol in self.__definedSymbols:
            self.__parent.__symbols[symbol] = self.getValue(symbol)
            self.__parent.__definedSymbols.add(symbol)
        
        return self.__parent


    def toDict(self):
        """
        Restituisce una rappresentazione come dizionario della memoria.
        Una modifica al dizionario restituito non si ripercuote sulla memoria.
        """
        symbolValueDict = dict(self.__symbols)
        if self.__parent:
            symbolValueDict.update(self.__parent.toDict())
        return symbolValueDict
    

    def __repr__(self):
        return str(self.toDict())
