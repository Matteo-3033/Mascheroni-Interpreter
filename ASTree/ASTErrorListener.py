from antlr4.error.ErrorListener import ErrorListener
from antlr4.error.Errors import *


class ASTErrorListener (ErrorListener):

    def __init__(self) -> None:
        super().__init__()

    def reportAmbiguity(self, recognizer, dfa, startIndex, stopIndex, exact, ambigAlts, configs):
        #print("reportAmbiguity")
        return super().reportAmbiguity(recognizer, dfa, startIndex, stopIndex, exact, ambigAlts, configs)
    
    def reportAttemptingFullContext(self, recognizer, dfa, startIndex, stopIndex, conflictingAlts, configs):
        #print("reportAttemptingFullContext")
        return super().reportAttemptingFullContext(recognizer, dfa, startIndex, stopIndex, conflictingAlts, configs)

    def reportContextSensitivity(self, recognizer, dfa, startIndex, stopIndex, prediction, configs):
        #print("reportContextSensitivity")
        return super().reportContextSensitivity(recognizer, dfa, startIndex, stopIndex, prediction, configs)

    def syntaxError(self, recognizer, offendingSymbol, line, column, msg, e):
        if e is None:  # Il parser ha corretto automaticamente l'errore
            print("SyntaxWarning - Linea: " + str(line) + ", col: " + str(column) + " - " + msg + ".")
            print("Correzione automatica dell'errore.")
        else:  # Non è stato corretto
            raise SyntaxError("Linea: " + str(line) + ", col: " + str(column) + " - " + msg + ".")
