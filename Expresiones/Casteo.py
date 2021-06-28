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
            try:
                return self.obtenerValor(self.tipo, value)
            except:
                return Excepcion("Semantico", "No se puede castear a int", self.fila, self.columna)
        elif self.tipo == TIPO.DECIMAL and self.expresion.tipo == TIPO.ENTERO: # int a double
            try:
                return self.obtenerValor(self.tipo, value)
            except:
                return Excepcion("Semantico", "No se puede castear a double", self.fila, self.columna)
        elif self.tipo == TIPO.CADENA and self.expresion.tipo == TIPO.ENTERO: #int a string
            try:
                return self.obtenerValor(self.tipo, value)
            except:
                return Excepcion("Semantico", "No se puede castear a string", self.fila, self.columna)
        elif self.tipo == TIPO.CHARACTER and self.expresion.tipo == TIPO.ENTERO: #entero a char
            try:
                return chr(self.obtenerValor(self.expresion.tipo, value))
            except:
                return Excepcion("Semantico", "No se puede castear a char", self.fila, self.columna)
        elif self.tipo == TIPO.CADENA and self.expresion.tipo == TIPO.DECIMAL: #decimal a cadena
            try:
                return self.obtenerValor(self.tipo, value)
            except:
                return Excepcion("Semantico", "No se puede castear a string", self.fila, self.columna)
        elif self.tipo == TIPO.ENTERO and self.expresion.tipo == TIPO.CHARACTER: #char a int
            try:
                return ord(value)
            except:
                return Excepcion("Semantico", "No se puede castear a int", self.fila, self.columna)
        elif self.tipo == TIPO.DECIMAL and self.expresion.tipo == TIPO.CHARACTER: #char a double
            try:
                numeroChar = ord(value)
                return self.obtenerValor(self.tipo, numeroChar)
            except:
                return Excepcion("Semantico", "No se puede castear a double", self.fila, self.columna)
        elif self.tipo == TIPO.ENTERO and self.expresion.tipo == TIPO.CADENA:  #string a int
            try:
                return int(self.obtenerValor(self.tipo, value))
            except:
                return Excepcion("Semantico", "No se puede castear a int", self.fila, self.columna)
        elif self.tipo == TIPO.DECIMAL and self.expresion.tipo == TIPO.CADENA:
            try:
                return float(self.obtenerValor(self.tipo, value))
            except:
                return Excepcion("Semantico", "No se puede castear a double", self.fila, self.columna)
        elif self.tipo == TIPO.BOOLEANO and self.expresion.tipo == TIPO.CADENA:
            try:
                if value.lower() == "true":
                    nuevoValor = True
                elif value.lower() == "false":
                    nuevoValor = False

                if nuevoValor == True or nuevoValor == False:
                    return nuevoValor
                else:
                    return Excepcion("Semantico", "No se puede castear a boolean", self.fila, self.columna)
            except:
                return Excepcion("Semantico", "No se puede castear a boolean", self.fila, self.columna)
        return Excepcion("Semantico", f"Imposible realizar castedo de [{self.expresion.tipo}] a [{self.tipo}]", self.fila, self.columna)


    def obtenerValor(self, tipo, valor):
        if tipo == TIPO.ENTERO:
            return int(valor)
        elif tipo == TIPO.DECIMAL:
            return float(valor)
        elif tipo == TIPO.CADENA:
            return str(valor)
        elif tipo == TIPO.CHARACTER:
            return str
        return Excepcion("Semantico", "No es posible realizar el casteo")