from Abstract.NodoAST import NodoAST
from Abstract.Instruccion import Instruccion

class Primitivos(Instruccion):
    def __init__(self, tipo, valor, fila, columna):
        self.tipo = tipo
        self.valor = valor
        self.fila = fila
        self.columna = columna

    def interpretar(self, tree, table):
        return self.valor  #retornar el valor(obtenido en la gramatica) del dato primitivo

    def getNodo(self):
        nodo = NodoAST("PRIMITIVO")
        nodo.agregarHijo(str(self.valor))
        return nodo