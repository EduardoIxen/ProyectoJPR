import re
from TS.Tipo import TIPO
from TS.Excepcion import Excepcion
from Abstract.Instruccion import Instruccion


class Casteo(Instruccion):
    def __init__(self, tipo, expresion, fila, columna):
        self.tipo = tipo
        self.expresion = expresion
        self.fila = fila
        self.columna = columna

    def interpretar(self, tree, table):
        value = self.expresion.interpretar(tree, table)
        if isinstance(value, Excepcion): return value

        if self.tipo == TIPO.ENTERO and self.expresion.tipo == TIPO.DECIMAL: #double a int
            return self.obtenerValor(self.tipo, value)
        elif self.tipo == TIPO.DECIMAL and self.expresion.tipo == TIPO.ENTERO: # int a double
            return self.obtenerValor(self.tipo, value)
        elif self.tipo == TIPO.CADENA and self.expresion.tipo == TIPO.ENTERO: #int a string
            return self.obtenerValor(self.tipo, value)
        elif self.tipo == TIPO.CHARACTER and self.expresion.tipo == TIPO.ENTERO: #entero a char
            return chr(self.obtenerValor(self.expresion.tipo, value))
        elif self.tipo == TIPO.CADENA and self.expresion.tipo == TIPO.DECIMAL: #decimal a cadena
            return self.obtenerValor(self.tipo, value)
        elif self.tipo == TIPO.ENTERO and self.expresion.tipo == TIPO.CHARACTER: #char a int
            return ord(value)
        elif self.tipo == TIPO.DECIMAL and self.expresion.tipo == TIPO.CHARACTER: #char a double
            numeroChar = ord(value)
            return self.obtenerValor(self.tipo, numeroChar)
        return Excepcion("Semantico", f"Imposible realizar castedo de [{self.expresion.tipo}] a [{self.tipo}]", self.fila, self.columna)


    def obtenerValor(self, tipo, valor):
        if tipo == TIPO.ENTERO:
            return int(valor)
        elif tipo == TIPO.DECIMAL:
            return float(valor)
        elif tipo == TIPO.CADENA:
            print("cadena")
            return str(valor)
        elif tipo == TIPO.CHARACTER:
            return str
        return Excepcion("Semantico", "No es posible realizar el casteo")