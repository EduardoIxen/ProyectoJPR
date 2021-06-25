from TS.Excepcion import Excepcion
from TS.Tipo import TIPO

class TablaSimbolos:
    def __init__(self, anterior = None):
        self.tabla = {} # Diccionario Vacio
        self.anterior = anterior

    def setTabla(self, simbolo):      # Agregar una variable a la tabla de símbolos
        if simbolo.id.lower() in self.tabla :
            return Excepcion("Semantico", "Variable " + simbolo.id + " ya existe", simbolo.fila, simbolo.columna)
        else:
            self.tabla[simbolo.id.lower()] = simbolo
            return None

    def getTabla(self, id):                     # obtener una variable de la tabla de simbolos por su id
        tablaActual = self
        while tablaActual != None:
            if id.lower() in tablaActual.tabla :
                return tablaActual.tabla[id.lower()]    #retorna el símbolo encontrado
            else:
                tablaActual = tablaActual.anterior
        return None

    '''
        # Actualizar el valor de un simbolo, buscando en la tabla de simbolos actual
        # y en las anteriores; comparando que el tipo anterior sea el mismo, Null ó
        # se le asigne valor null
    '''
    def actualizarTabla(self, simbolo):
        tablaActual = self
        while tablaActual != None:
            if simbolo.id.lower() in tablaActual.tabla :
                if tablaActual.tabla[simbolo.id.lower()].getTipo() == simbolo.getTipo() or \
                    simbolo.getTipo() == TIPO.NULO or tablaActual.tabla[simbolo.id.lower()].getTipo() == TIPO.NULO:
                    tablaActual.tabla[simbolo.id.lower()].setValor(simbolo.getValor())
                    tablaActual.tabla[simbolo.id.lower()].setTipo(simbolo.getTipo())
                    return None   ### VARIABLE ACTUALIZADA
                return Excepcion("Semantico", f"Tipo de dato diferente para la asignacion [{self.tabla[simbolo.id].getValor()} ({self.tabla[simbolo.id].getTipo()}) -> {simbolo.getValor()} ({simbolo.getTipo()})]", simbolo.getFila(), simbolo.getColumna())
            else:
                tablaActual = tablaActual.anterior
        return Excepcion("Semantico", f"Variable no encontrada en asignacion -{simbolo.id}-.", simbolo.getFila(), simbolo.getColumna())
        