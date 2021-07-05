from Abstract.NodoAST import NodoAST
from TS.Excepcion import Excepcion
from Abstract.Instruccion import Instruccion
from TS.Simbolo import Simbolo
from TS.Tipo import TIPO
import copy
import numpy

class DeclaracionReferencia(Instruccion):
    def __init__(self, tipo, dimensiones, identificador, idReferencia, fila, columna):
        self.identificador = identificador
        self.tipo = tipo
        self.dimensiones = dimensiones
        self.idReferencia = idReferencia
        self.fila = fila
        self.columna = columna
        self.arreglo = True
        self.valor = "null"


    def interpretar(self, tree, table):
        simbolo = table.getTabla(self.idReferencia.lower())
        if simbolo == None:
            return Excepcion("Semantico", "Variable " + self.identificador + " no encontrada.", self.fila, self.columna)

        #tipo del arreglo llamado
        if self.tipo != simbolo.getTipo():
            return Excepcion("Semantico", "Tipo de dato diferente al del Arreglo.", self.fila, self.columna)
        
        dimenSimb = numpy.array(simbolo.getValor())
        self.valor = simbolo.getValor()

        if self.dimensiones != len(dimenSimb.shape):
            return Excepcion("Semantico", "Dimensiones incompatibles entre arreglos.", self.fila, self.columna)

        simbolo.setID(self.identificador)
        result = table.setTabla(simbolo)
        if isinstance(result, Excepcion): return result
        return None

    def getNodo(self):
        nodo = NodoAST("DECLARACION ARREGLO")
        nodo.agregarHijo(str(self.tipo))
        nodo.agregarHijo(str(self.dimensiones))
        nodo.agregarHijo(str(self.identificador))
        
        return nodo


    def getTabla(self,tree,table, padre):
        from TS.TablaSimbolos import listaTablaSimbolos
        salida = ""

        dic = {}
        dic['Identificador'] = str(self.identificador)
        dic['Tipo'] = "Variable"
        dic['Tipo2'] = str(self.tipo).replace("TIPO.", "ARREGLO->")
        dic['Entorno'] = str(padre)
        dic['Valor'] = str(self.valor)
        dic['Fila'] = str(self.fila)
        dic['Columna'] = str(self.columna)
        
        listaTablaSimbolos.append(dic)
        
        return salida