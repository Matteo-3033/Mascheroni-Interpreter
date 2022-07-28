import Memory as mem
from ASTree.ASTVisitor import ASTVisitor
from ASTree.ASTErrorListener import ASTErrorListener

import geometry

import operator
from functools import partial
from typing import Any

from antlr4.CommonTokenStream import CommonTokenStream
from antlr4.InputStream import InputStream
from Grammatica.MascheroniLexer import MascheroniLexer
from Grammatica.MascheroniParser import MascheroniParser


class Interpreter:
    """
    Interprete per eseguire codice scritto in linguaggio di Mascheroni.
    Per eseguire un codice sorgente è necessario passarlo all'interprete tramite il metodo source(str)
    e quindi, se il metodo restituisce True, invocare il metodo eval (o l'operatore di call dell'interprete);
    il risultato della computazione è salvato nel file indicato dall'attributo OUTPUT_FILE_NAME.
    
    L'input del construct main può essere passato direttamente tramite il metodo eval (i punti come tuple di due interi, gli altri enti come tuple di due tuple di due interi) oppoure generato casualmente.
    In quest'ultimo caso tutti i punti generati hanno coordinate intere e appartengono di base a un quadrato col vertice
    in basso a sinistra nell'origine e lato 100, ma il range può essere modificato attraverso gli attributi MIN_X, MAX_X,
    MIN_Y, MAX_Y. Nel modificare questi parametri è necessario fare attenzione a non definire un'area troppo piccola in cui
    non è possibile individuare abbastanza punti; in questo caso l'interprete non terminerebbe l'esecuzione.
    I punti eventualmente generati casualmente non sono mai tra loro allinati orizzontalmente o verticalmente, mentre
    le rette che passano per i punti che definiscono segments, rays, lines e circles non sono mai né parallele né perpendicolari tra loro.

    L'interprete si trova in ogni istante in uno tra due stati, running e notRunning, che permettono o impediscono
    l'esecuzione di certi metodi. Nello stato notRunning, quello in cui si trova un interprete appena creato,
    in particolare i metodi eseguibili sono source, eval, printAST, reset e freeMemory.
    """

    # Dispatch table degli operatori:
    opDT = {
        "=="    : operator.eq,
        "!="    : operator.ne,
        ">"     : operator.gt,
        ">="    : operator.ge,
        "<"     : operator.lt,
        "<="    : operator.le,
        "*"     : operator.mul,
        "/"     : operator.floordiv,
        "%"     : operator.mod,
        "+"     : operator.add,
        "-"     : operator.sub,
        "!"     : operator.not_,
        "^"     : geometry.intersection,
        "^0"    : partial(geometry.intersection, which_one = 0),
        "^1"    : partial(geometry.intersection, which_one = 1)
    }

    # Insieme dei tipi geometrici:
    GEOMETRY_TYPES = {"point", "segment", "ray", "line", "circle"}

    # Valori minimi e massimi delle coordinate degli input generati casualmente:
    MIN_X = 0
    MAX_X = 100
    MIN_Y = 0
    MAX_Y = 100

    # Nome del file in cui salvare il risultato:
    OUTPUT_FILE_NAME = "mascheroni.html"

    def __init__(self):
        self.__ast = None                       # AST relativo al codice sorgente passato all'interprete
        self.__sourceCode = None                # Codice da interpretare

        self.__actRecorsStack = [mem.Memory()]  # Stack dei record di attivazione
        self.activeConstructs = set()           # Insieme dei construct attivi
        self.__svg = ""                         # Stringa svg prodotta dalle istruzioni "show"
        self.constructsTable = mem.Memory()     # Memoria dei constructs
        self.inputs = []                        # Lista delgli input passati all'interprete
        
        self.currentConstructName = None        # Riferimento al nodo radice del constructs corrente
        self.__running = False                  # True durante l'interpretazione del codice        
        self.__isMemoryFree = True              # True se la memoria è libera e il codice può quindi essere eseguito


    def source(self, source: str):
        """
        Definisce il codice sorgente da eseguire e ne esegue il parsing.
        Restituisce True se l'operazione termina correttamente ed è possibile invocare
        il metodo eval, False altrimenti.
        """
        if self.__running:
            raise InvalidStateError(self.__running, self.source.__name__)
        
        if self.__ast is not None:
            self.reset()
        
        if not isinstance(source, str):
            raise TypeError(
                f"Interprete - Il codice sorgente deve essere passato sotto forma di stringa, non {type(source)}."
            )

        source = source.strip()
        sourceSplitted = source.split("\n")
        # Sostituisco i caratteri ∩ con ^ per problemi di encoding:
        source = source.strip().replace('∩', '^')

        try:
            # Generazione dell'albero di parsing tramite ANTLR:
            lexer = MascheroniLexer(InputStream(source))
            stream = CommonTokenStream(lexer)
            lexer.reset()
            parser = MascheroniParser(stream)
            parser.removeErrorListeners()
            parser.addErrorListener(ASTErrorListener())
            antlr_tree = parser.start()

            # Visita dell'albero e generazione dell'AST:
            visitor = ASTVisitor()
            self.__ast = visitor.visit(antlr_tree)

        except BaseException as e:
            self.__error(e)
            return False
        
        # Salvataggio del codice sorgente per la generazione successiva del file di output:
        self.__sourceCode = "\n".join([str(i+1) + "\t" + sourceSplitted[i] for i in range(len(sourceSplitted))])

        return True


    def eval(self, inputs = list()):
        """
        Esegue il codice passato tramite il metodo source sugli input in inputs e ne salva il risultato
        nel file indicato da OUTPUT_FILE_NAME.
        Se il numero di input nella lista è minore di quelli richiesti i restanti necessari vengono generati casualmente.
        """
        if self.__running:
            raise InvalidStateError(self.__running, self.eval.__name__)
        
        if not self.__ast:
            raise RuntimeError("Interprete - Codice sorgente mancante: passarlo tramite il metodo source(str).")
        
        if not self.__isMemoryFree:
            self.freeMemory()
        
        
        # Salva la lista di input perché sia accessibile dall'AST.
        # Il controllo della loro validità è effettuato direttamente dal nodo radice dell'AST.
        self.inputs = list(inputs)

        self.__running = True

        try:
            self.__ast.setRandomInputRange(
                self.MIN_X,
                self.MAX_X,
                self.MIN_Y,
                self.MAX_Y
            )
            outputs = self.__ast.visit(self)
        except BaseException as e:
            self.__error(e)
            return
        
        self.__running = False
        self.__isMemoryFree = False

        # Salvataggio dei risultati:
        try:
            with open(self.OUTPUT_FILE_NAME, "w", encoding= "utf-8") as file:
                file.write(f"""<html><body>
                    <h1>Source:</h1><pre>{self.__sourceCode}</pre>
                    <h1>Input:</h1><pre>{self.inputs}</pre>
                    {f"<h1>Output:</h1><pre>{[output[0] for output in outputs]}</pre>" if outputs else ""}
                    {f"<h1>Show:</h1>{self.__svg}" if self.__svg else ""}
                    </body></html>
                """)
        except:
            print(
                f"Interpreter - Impossibile salvare l'output del programma nel file {self.OUTPUT_FILE_NAME}: controllare che il percorso specificato sia corretto."
            )
            return
        
        print(f"Risultati salvati in \"{self.OUTPUT_FILE_NAME}\".")
    

    def __error(self, e: BaseException):
        """
        Stampa il messaggio di errore dell'eccezione passata in input.
        """
        print(f'{type(e).__name__}{", " + self.currentConstructName if self.currentConstructName else ""} - {str(e)}')


    def printAST(self):
        """
        Stampa una rappresentazione grafica dell'AST relativo al codice sorgento passato
        tramite il metodo source(str).
        """
        if self.__ast:
            print(self.__ast)
        else:
            raise RuntimeError(
                "Interprete - AST non definito: utilizzare il metodo source(str) per passare il sorgente da cui generare l'AST."
            )

    @property
    def actRecord(self):
        """
        Restituisce il record di attivazione corrente.
        """
        if not self.__running: return None
        return self.__actRecorsStack[-1]
        

    def newActRecord(self):
        """
        Crea un nuovo record di attivazione e lo imposta come corrente.
        """
        if not self.__running:
            raise InvalidStateError(self.__running, self.newActRecord.__name__)

        self.__actRecorsStack.append(mem.Memory())

    
    def discardActRecord(self):
        """
        Ripristina il precedente record di attivazione scartando quello corrente.
        Da invocare in seguito a una chiamata a newActRecord().
        """
        if not self.__running:
            raise InvalidStateError(self.__running, self.discardActRecord.__name__)

        if len(self.__actRecorsStack) <= 1:
            raise MemoryError("Nessun record di attivazione da ripristinare.")
            
        self.__actRecorsStack.pop()


    def enterScope(self):
        """
        Crea un nuovo scope in memoria.
        """
        if not self.__running:
            raise InvalidStateError(self.__running, self.enterScope.__name__)

        self.__actRecorsStack[-1] = self.__actRecorsStack[-1].enterScope()
    

    def exitScope(self):
        """
        Elimina l'ultimo scope creato tramite il metodo "enterScope()".
        """
        if not self.__running:
            raise InvalidStateError(self.__running, self.exitScope.__name__)

        self.__actRecorsStack[-1] = self.__actRecorsStack[-1].exitScope()
    

    def show(self, svg: str):
        """
        Accetta in input una stringa in formato svg e ne aggiunge il contenuto al file di output dell'interprete.
        """
        if not self.__running:
            raise InvalidStateError(self.__running, self.show.__name__)

        if len(svg) == 0: return
        self.__svg = f'<fieldset style="border: 1pt dashed black; margin: .5em 0;"><legend>{self.currentConstructName}</legend>{self.__svg}<div>{svg}</div></fieldset>'
        

    def reset(self):
        """
        Ripristina l'interprete eliminando tutte le informazioni relative all'ultimo sorgente definito.
        """
        if self.__running:
            raise InvalidStateError(self.__running, self.reset.__name__)
        
        self.__ast = None
        self.sourceCode = None
        
        self.MIN_X = 0
        self.MAX_X = 100
        self.MIN_Y = 0
        self.MAX_Y = 100
        self.OUTPUT_FILE_NAME = "mascheroni.html"

        self.freeMemory()


    def freeMemory(self):
        """
        Pulisce la memoria dell'interprete per poter rieseguire il codice su nuovi input.
        """
        if self.__running:
            raise InvalidStateError(self.__running, self.freeMemory.__name__)

        if self.__isMemoryFree:
            return

        self.currentConstructName = None
        self.activeConstructs = set()
        self.inputs.clear()
        self.__svg = ""
        self.__actRecorsStack.clear()
        self.__actRecorsStack.append(mem.Memory())
        self.constructsTable = mem.Memory()
        
        self.__isMemoryFree = True


    def __call__(self, *args: Any):
        """
        Si veda Interpreter.eval(args)
        """
        return self.eval(args)
        


class InvalidStateError(RuntimeError):
    """
    Eccezione sollevata quando viene invocato un metodo di un oggetto della classe Interpreter,
    ma l'interprete non si trova nello stato necessario per la sua esecuzione.
    """

    def __init__(self, running: bool, method: str):
        self.__running = bool(running)
        self.__method = method


    def __repr__(self) -> str:
        return str(self)
    

    def __str__(self) -> str:
        return f"Interprete - Stato non valido: il metodo {self.__method} non può essere invocato se l'interprete " + ("" if self.__running else "non ") + "è in esecuzione."
