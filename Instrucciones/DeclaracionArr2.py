from Abstract.NodoAST import NodoAST
from TS.Excepcion import Excepcion
from Abstract.Instruccion import Instruccion
from TS.Simbolo import Simbolo
from TS.Tipo import TIPO
import copy


class DeclaracionArr2(Instruccion):
    def __init__(self, tipo, dimensiones, identificador, expresiones, fila, columna):
        self.identificador = identificador
        self.tipo = tipo
        self.dimensiones = dimensiones
        self.expresiones = expresiones
        self.fila = fila
        self.columna = columna
        self.arreglo = True


    def interpretar(self, tree, table):
        print("tipo->",self.tipo)
        print("dimen-> ", self.dimensiones)
        print("id", self.identificador)
        print("expresiones", self.expresiones)
        temp = self.expresiones
        #for tp in temp:
        #    print(tp.valor)
        
        value = self.crearArreglo(tree, table, copy.copy(self.expresiones), None)
        simbolo = Simbolo(str(self.identificador), self.tipo, self.arreglo, self.fila, self.columna, value)
        result = table.setTabla(simbolo)
        if isinstance(result, Excepcion): return result
        print("nada")
        return None

    def getNodo(self):
        nodo = NodoAST("DECLARACION ARREGLO 2")
        nodo.agregarHijo(str(self.identificador))
        return nodo

    def crearArreglo(self, tree, table, expresiones, valorActual):
        pass


'''
arr = []
        if len(expresiones) == 0:
            return valorActual.interpretar(tree, table)

        dimencion = expresiones.pop(0)
        print("dimencion",dimencion)
        num = len(dimencion)
        contador = 0
        while contador < num:
            arr.append(self.crearArreglo(tree, table, copy.copy(expresiones), copy.copy(dimencion[contador])))
            contador += 1
        return arr
'''