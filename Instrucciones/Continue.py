from TS.Excepcion import Excepcion
from Abstract.Instruccion import Instruccion

class Continue(Instruccion):
    def __init__(self, fila, columna):
        self.fila = fila
        self.columna = columna

    def interpretar(self, tree, table):
        return self