from Instrucciones.Funcion import Funcion
from TS.Excepcion import Excepcion
from TS.Tipo import TIPO
import math

class Round(Funcion):
    def __init__(self, identificador, parametros, instrucciones, fila, columna):
        self.identificador = identificador.lower()
        self.parametros = parametros
        self.instrucciones = instrucciones
        self.fila = fila
        self.columna = columna
        self.tipo = TIPO.NULO
    
    def interpretar(self, tree, table):
        simbolo = table.getTabla("round##Param1")
        if simbolo == None: return Excepcion("Semantico", "No se encontro parametro de ToLower.", self.fila, self.columna)

        if simbolo.getTipo() != TIPO.DECIMAL and simbolo.getTipo() != TIPO.ENTERO:
            return Excepcion("Semantico", "Parametro de Truncate no es numerico", self.fila, self.columna)
        
        self.tipo = TIPO.ENTERO
        return int(self.roundNum(simbolo.getValor()))

    def roundNum(self, numero):
        decimal, entero = math.modf(numero)
        if decimal >= 0.5:
            return entero + 1
        else:
            return entero
        