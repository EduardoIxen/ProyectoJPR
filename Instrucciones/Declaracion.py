from TS.Tipo import TIPO
from tkinter.constants import NO
from TS.Excepcion import Excepcion
from Abstract.Instruccion import Instruccion
from TS.Simbolo import Simbolo

class Declaracion(Instruccion):
    def __init__(self, identificador, fila, columna, expresion=None):
        self.identificador = identificador
        self.expresion = expresion
        self.fila = fila
        self.columna = columna

    def interpretar(self, tree, table):
        if self.expresion != None:
            value = self.expresion.interpretar(tree, table) #Valor a asignar a la variable
            tipo = self.expresion.tipo

            if isinstance(value, Excepcion): return value

            simbolo = Simbolo(str(self.identificador), tipo, self.fila, self.columna, value)

            result = table.setTabla(simbolo)

            if isinstance(result, Excepcion): return result
            return None
        else:
            value = "null"
            tipo = TIPO.NULO

            if isinstance(value, Excepcion): return value

            simbolo = Simbolo(str(self.identificador), tipo, self.fila, self.columna, value)
            result = table.setTabla(simbolo)
            if isinstance(result, Excepcion): return result
            return None
        