
from Abstract.NodoAST import NodoAST
from TS.Tipo import TIPO
from tkinter.constants import NO
from TS.Excepcion import Excepcion
from Abstract.Instruccion import Instruccion
from TS.Simbolo import Simbolo

class Declaracion(Instruccion):
    def __init__(self, identificador, fila, columna, expresion=None):
        self.identificador = identificador
        self.expresion = expresion
        self.fila = fila
        self.columna = columna
        self.arreglo = False
        self.tipo = None
        self.valor = None

    def interpretar(self, tree, table):
        if self.expresion != None:
            value = self.expresion.interpretar(tree, table) #Obtener el valor de la expresio para asignar a la variable

            if isinstance(value, Excepcion): return value
            tipo = self.expresion.tipo
            self.tipo = tipo
            self.valor = value
            simbolo = Simbolo(str(self.identificador), tipo, self.arreglo, self.fila, self.columna, value)

            result = table.setTabla(simbolo) #Agregar el nuevo simbolo a la tabla de simbolos

            if isinstance(result, Excepcion): return result
            return None
        else:
            value = "null"  #asignamos null porque no tiene la expresion definida
            tipo = TIPO.NULO
            self.tipo = tipo
            self.valor = "null"

            if isinstance(value, Excepcion): return value

            simbolo = Simbolo(str(self.identificador), tipo, self.arreglo, self.fila, self.columna, value)
            result = table.setTabla(simbolo)
            if isinstance(result, Excepcion): return result
            return None
        
    def getNodo(self):
        nodo = NodoAST("DECLARACION")
        nodo.agregarHijo(str(self.identificador))
        if self.expresion != None:
            nodo.agregarHijoNodo(self.expresion.getNodo())
        return nodo

    def getTabla(self,tree,table, padre):
        from TS.TablaSimbolos import listaTablaSimbolos
        salida = ""
        nombre = "Main"
        nombreFunc = "Funcion"

        salida += "-¿¿¿Declaracion¿¿¿" + self.identificador + "¿¿¿"+ str(self.tipo)  + "¿¿¿" + str(self.fila) + "¿¿¿"+ str(self.columna)+ "¿¿¿ - &&\n"

        dic = {}
        dic['Identificador'] = str(self.identificador)
        dic['Tipo'] = "Variable"
        dic['Tipo2'] = str(self.tipo).replace("TIPO.", "")
        dic['Entorno'] = str(padre)
        dic['Valor'] = str(self.valor)
        dic['Fila'] = str(self.fila)
        dic['Columna'] = str(self.columna)
        
        listaTablaSimbolos.append(dic)
        
        return salida