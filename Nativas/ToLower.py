from Abstract.NodoAST import NodoAST
from Instrucciones.Funcion import Funcion
from Instrucciones.Return import Return
from Abstract.Instruccion import Instruccion
from TS.TablaSimbolos import TablaSimbolos
from TS.Excepcion import Excepcion
from Instrucciones.Break import Break
from TS.Tipo import TIPO

class Tolower(Funcion):
    def __init__(self, identificador, parametros, instrucciones, fila, columna):
        self.identificador = identificador.lower()
        self.parametros = parametros
        self.instrucciones = instrucciones
        self.fila = fila
        self.columna = columna
        self.tipo = TIPO.NULO
        self.simbolo = None
    
    def interpretar(self, tree, table):
        simbolo = table.getTabla("toLower##Param1")
        if simbolo == None: return Excepcion("Semantico", "No se encontro parametro de ToLower.", self.fila, self.columna)

        self.simbolo = simbolo
        if simbolo.getTipo() != TIPO.CADENA:
            return Excepcion("Semantico", "Parametro de ToLower no es cadena", self.fila, self.columna)
        
        self.tipo = simbolo.getTipo()
        try:
            return simbolo.getValor().lower()
        except:
            return Excepcion("Semantico", "Parametro de ToLower no es cadena", self.fila, self.columna)

    def getNodo(self):
        nodo = NodoAST("TOLOWER")
        nodoDato = NodoAST(self.simbolo.getTipo())
        nodoDato.agregarHijo(self.simbolo.getValor())
        nodo.agregarHijoNodo(nodoDato)
        return nodo