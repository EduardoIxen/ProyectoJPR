from Abstract.NodoAST import NodoAST
from TS.Excepcion import Excepcion
from TS.TablaSimbolos import TablaSimbolos
from Abstract.Instruccion import Instruccion

class Return(Instruccion):
    def __init__(self, expresion, fila, columna):
        self.expresion = expresion
        self.fila = fila
        self.columna = columna
        self.tipo = None
        self.result = None

    def interpretar(self, tree, table):
        result = self.expresion.interpretar(tree, table)
        if isinstance(result, Excepcion): return result 

        self.tipo = self.expresion.tipo #tipo del result
        self.result = result            # valor del result

        return self

    def getNodo(self):
        nodo = NodoAST("RETURN")
        nodo.agregarHijoNodo(self.expresion.getNodo())
        return nodo