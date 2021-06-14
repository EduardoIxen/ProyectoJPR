from TS.Excepcion import Excepcion
from TS.Tipo import TIPO

class TablaSimbolos:
    def __init__(self, anterior = None):
        self.tabla = {} # Diccionario Vacio
        self.anterior = anterior
        self.funciones = []

    def setTabla(self, simbolo):      # Agregar una variable
        if simbolo.id.lower() in self.tabla :
            return Excepcion("Semantico", "Variable " + simbolo.id + " ya existe", simbolo.fila, simbolo.columna)
        else:
            self.tabla[simbolo.id.lower()] = simbolo
            return None

    def getTabla(self, id):            # obtener una variable
        tablaActual = self
        while tablaActual != None:
            if id in tablaActual.tabla :
                return tablaActual.tabla[id]    #retorna simbolo
            else:
                tablaActual = tablaActual.anterior
        return None

    def actualizarTabla(self, simbolo):
        tablaActual = self
        while tablaActual != None:
            if simbolo.id in tablaActual.tabla :
                if tablaActual.tabla[simbolo.id].getTipo() == simbolo.getTipo() or \
                    simbolo.getTipo() == TIPO.NULO or tablaActual.tabla[simbolo.id].getTipo() == TIPO.NULO:
                    tablaActual.tabla[simbolo.id].setValor(simbolo.getValor())
                    tablaActual.tabla[simbolo.id].setTipo(simbolo.getTipo())
                    return None   ### VARIABLE ACTUALIZADA
                return Excepcion("Semantico", f"Tipo de dato diferente para la asignacion [{self.tabla[simbolo.id].getValor()} ({self.tabla[simbolo.id].getTipo()}) -> {simbolo.getValor()} ({simbolo.getTipo()})]", simbolo.getFila(), simbolo.getColumna())
            else:
                tablaActual = tablaActual.anterior
        return Excepcion("Semantico", f"Variable no encontrada en asignacion.", simbolo.getFila(), simbolo.getColumna())
        