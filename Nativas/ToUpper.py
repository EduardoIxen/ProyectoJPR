from Abstract.NodoAST import NodoAST
from Instrucciones.Funcion import Funcion
from Instrucciones.Return import Return
from Abstract.Instruccion import Instruccion
from TS.TablaSimbolos import TablaSimbolos
from TS.Excepcion import Excepcion
from Instrucciones.Break import Break
from TS.Tipo import TIPO

class ToUpper(Funcion):
    def __init__(self, identificador, parametros, instrucciones, fila, columna):
        self.identificador = identificador.lower()
        self.parametros = parametros
        self.instrucciones = instrucciones
        self.fila = fila
        self.columna = columna
        self.tipo = TIPO.NULO
        self.simbolo = None
    
    def interpretar(self, tree, table):
        simbolo = table.getTabla("toUpper##Param1")  #buscar por el id quemado del parametro de la funcion
        if simbolo == None: return Excepcion("Semantico", "No se encontro parametro de ToUpper.", self.fila, self.columna)

        if simbolo.getTipo() != TIPO.CADENA:
            return Excepcion("Semantico", "Parametro de ToUpper no es cadena", self.fila, self.columna)
        
        self.simbolo = simbolo
        self.tipo = simbolo.getTipo()
        try:
            return simbolo.getValor().upper()
        except:
            return Excepcion("Semantico", "Parametro de ToUpper no es cadena", self.fila, self.columna)

    def getNodo(self):
        nodo = NodoAST("TOUPPER")
        nodoDato = NodoAST(self.simbolo.getTipo())
        nodoDato.agregarHijo(self.simbolo.getValor())
        nodo.agregarHijoNodo(nodoDato)
        return nodo