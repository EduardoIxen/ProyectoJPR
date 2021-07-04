from Abstract.NodoAST import NodoAST
from Instrucciones.Funcion import Funcion
from Instrucciones.Return import Return
from Abstract.Instruccion import Instruccion
from TS.TablaSimbolos import TablaSimbolos
from TS.Excepcion import Excepcion
from Instrucciones.Break import Break
from TS.Tipo import TIPO

class Length(Funcion):
    def __init__(self, identificador, parametros, instrucciones, fila, columna):
        self.identificador = identificador.lower()
        self.parametros = parametros
        self.instrucciones = instrucciones
        self.fila = fila
        self.columna = columna
        self.tipo = TIPO.NULO
        self.simbolo = None
    
    def interpretar(self, tree, table):
        simbolo = table.getTabla("length##Param1")
        if simbolo == None: return Excepcion("Semantico", "No se encontro parametro de length.", self.fila, self.columna)
        self.simbolo = simbolo
        self.tipo = TIPO.ENTERO
        if simbolo.getTipo() == TIPO.CADENA or isinstance(simbolo.getValor(), list):
            try:
                return len(simbolo.getValor())
            except:
                return Excepcion("Semantico", "Parametro de Legnth no es compatible", self.fila, self.columna)
        return Excepcion("Semantico", "Parametro de Legnth no es compatible", self.fila, self.columna)


    def getNodo(self):
        nodo = NodoAST("LENGTH")
        tipoDato = NodoAST(self.simbolo.getTipo())
        if self.simbolo.getTipo() == TIPO.CADENA:
            tipoDato.agregarHijo(self.simbolo.getValor())
        elif self.simbolo.getArreglo():
            tipoDato.agregarHijo(self.simbolo.getID())
        else:
            return Excepcion("Semantico", "Tipo de dato invalido para la funcion length", self.fila, self.columna)
        nodo.agregarHijoNodo(tipoDato)
        return nodo
