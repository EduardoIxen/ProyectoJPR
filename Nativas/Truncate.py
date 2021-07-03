from Abstract.NodoAST import NodoAST
from Instrucciones.Funcion import Funcion
from TS.Excepcion import Excepcion
from TS.Tipo import TIPO
import math

class Truncate(Funcion):
    def __init__(self, identificador, parametros, instrucciones, fila, columna):
        self.identificador = identificador.lower()
        self.parametros = parametros
        self.instrucciones = instrucciones
        self.fila = fila
        self.columna = columna
        self.tipo = TIPO.NULO
        self.simbolo = None
    
    def interpretar(self, tree, table):
        simbolo = table.getTabla("truncate##Param1")
        if simbolo == None: return Excepcion("Semantico", "No se encontro parametro de ToLower.", self.fila, self.columna)

        if simbolo.getTipo() != TIPO.DECIMAL and simbolo.getTipo() != TIPO.ENTERO:
            return Excepcion("Semantico", "Parametro de Truncate no es numerico", self.fila, self.columna)
        
        self.simbolo = simbolo
        self.tipo = TIPO.ENTERO

        return math.trunc(simbolo.getValor())

    def getNodo(self):
        nodo = NodoAST("TRUNCATE")
        nodoDato = NodoAST(self.simbolo.getTipo())
        nodoDato.agregarHijo(self.simbolo.getValor())
        nodo.agregarHijoNodo(nodoDato)
        return nodo