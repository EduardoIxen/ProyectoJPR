from Abstract.NodoAST import NodoAST
from TS.Excepcion import Excepcion
from Abstract.Instruccion import Instruccion
from TS.Simbolo import Simbolo
from TS.Tipo import TIPO
import copy


class AccesoArreglo(Instruccion):
    def __init__(self, identificador, expresiones, fila, columna):
        self.identificador = identificador
        self.expresiones = expresiones
        self.fila = fila
        self.columna = columna


    def interpretar(self, tree, table):
        simbolo = table.getTabla(self.identificador.lower())

        if simbolo == None:
            return Excepcion("Semantico", "Variable " + self.identificador + " no encontrada.", self.fila, self.columna)

        self.tipo = simbolo.getTipo()

        if not simbolo.getArreglo(): 
            return Excepcion("Semantico", "Variable " + self.identificador + " no es un arreglo.", self.fila, self.columna)


        # BUSQUEDA DEL ARREGLO
        value = self.buscarDimensiones(tree, table, copy.copy(self.expresiones), simbolo.getValor())     #RETORNA EL VALOR SOLICITADO
        if isinstance(value, Excepcion): return value
        #if isinstance(value, list):
        #    return Excepcion("Semantico", "Acceso a Arreglo incompleto.", self.fila, self.columna)

        return value

    def getNodo(self):
        nodo = NodoAST("ACCESO ARREGLO")
        nodo.agregarHijo(str(self.identificador))
        exp = NodoAST("EXPRESIONES DE LAS DIMENSIONES")
        for expresion in self.expresiones:
            exp.agregarHijoNodo(expresion.getNodo())
        nodo.agregarHijoNodo(exp)
        return nodo

    def buscarDimensiones(self, tree, table, expresiones, arreglo):
        value = None
        if len(expresiones) == 0:
            return arreglo
        if not isinstance(arreglo, list):
            return Excepcion("Semantico", "Accesos de más en un Arreglo.", self.fila, self.columna)
        dimension = expresiones.pop(0)
        num = dimension.interpretar(tree, table)
        if isinstance(num, Excepcion): return num
        if dimension.tipo != TIPO.ENTERO:
            return Excepcion("Semantico", "Expresion diferente a ENTERO en Arreglo.", self.fila, self.columna)

        try:
            value = self.buscarDimensiones(tree, table, copy.copy(expresiones), arreglo[num])
        except:
            Excepcion("Semantico", "Error al acceder a la posicion del arreglo.", self.fila, self.columna)

        return value
