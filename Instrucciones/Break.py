from Abstract.NodoAST import NodoAST
from Abstract.Instruccion import Instruccion

class Break(Instruccion):
    def __init__(self, fila, columna):
        self.fila = fila
        self.columna = columna

    def interpretar(self, tree, table):
        return self

    def getNodo(self):
        nodo = NodoAST("BREAK")
        return nodo