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
    
    def interpretar(self, tree, table):
        simbolo = table.getTabla("length##Param1")
        if simbolo == None: return Excepcion("Semantico", "No se encontro parametro de length.", self.fila, self.columna)

        self.tipo = TIPO.ENTERO
        if simbolo.getTipo() == TIPO.CADENA:
            return len(simbolo.getValor())

        return Excepcion("Semantico", "Parametro de Legnth no es compatible", self.fila, self.columna)