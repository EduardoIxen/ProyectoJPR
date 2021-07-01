from Abstract.NodoAST import NodoAST
from Abstract.Instruccion import Instruccion
from TS.Excepcion import Excepcion
from TS.Tipo import TIPO

class Imprimir(Instruccion):
    def __init__(self, expresion, fila, columna):
        self.expresion = expresion
        self.fila = fila
        self.columna = columna

    def interpretar(self, tree, table):
        value = self.expresion.interpretar(tree, table)  # RETORNA CUALQUIER VALOR DE UNA EXPRESION

        if isinstance(value, Excepcion) :
            return value

        if self.expresion.tipo == TIPO.ARREGLO:
            return Excepcion("Semantico", "No se puede imprimir un arreglo completo", self.fila, self.columna)
        
        tree.updateConsola(value) #agregar el valor a la salida de la consola
        return None

    def getNodo(self):
        nodo = NodoAST("IMPRIMIR")
        nodo.agregarHijoNodo(self.expresion.getNodo())
        return nodo