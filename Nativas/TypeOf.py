from Abstract.NodoAST import NodoAST
from Instrucciones.Funcion import Funcion
from TS.Excepcion import Excepcion
from TS.Tipo import TIPO

class TypeOf(Funcion):
    def __init__(self, identificador, parametros, instrucciones, fila, columna):
        self.identificador = identificador.lower()
        self.parametros = parametros
        self.instrucciones = instrucciones
        self.fila = fila
        self.columna = columna
        self.tipo = TIPO.NULO
        self.simbolo = None
    
    def interpretar(self, tree, table):
        simbolo = table.getTabla("typeof##Param1")  #buscar por el id quemado del parametro de la funcion
        if simbolo == None: return Excepcion("Semantico", "No se encontro parametro de Typeof.", self.fila, self.columna)
        
        self.simbolo = simbolo
        self.tipo = TIPO.CADENA
        try:
            if not isinstance(simbolo.getValor(), list):
                return self.obtenerTipo(simbolo.getTipo())
            else:
                return "ARREGLO->"+self.obtenerTipo(simbolo.getTipo())
        except:
            return Excepcion("Semantico", "Error al encontrar el tipo de dato.", self.fila, self.columna)


    def getNodo(self):
        nodo = NodoAST("TYPEOF")
        nodo.agregarHijo(self.simbolo.getID())
        return nodo

    def obtenerTipo(self, tipoEntrada):
        if tipoEntrada == TIPO.ENTERO:
            return "INT"
        elif tipoEntrada == TIPO.DECIMAL:
            return "DOUBLE"
        elif tipoEntrada == TIPO.BOOLEANO:
            return "BOOLEAN"
        elif tipoEntrada == TIPO.CHARACTER:
            return "CHAR"
        elif tipoEntrada == TIPO.CADENA:
            return "STRING"
        elif tipoEntrada == TIPO.NULO:
            return "NULL"
        elif tipoEntrada == TIPO.ARREGLO:
            return "ARREGLO"
        else:
            return Excepcion("Semantico", "Tipo de dato invalido.", self.fila, self.columna)