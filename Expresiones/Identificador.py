from Abstract.Instruccion import Instruccion
from TS.Excepcion import Excepcion

class Identificador(Instruccion):
    def __init__(self, identificador, fila, columna):
        self.identificador = identificador
        self.fila = fila
        self.columna = columna
        self.tipo = None

    def interpretar(self, tree, table):
        simbolo = table.getTabla(self.identificador.lower())  #OBTENER SIMBOLO DEL ID

        if simbolo == None:
            return Excepcion("Semantico", "Variable " + self.identificador + " no encontrada.", self.fila, self.columna)

        self.tipo = simbolo.getTipo()
        
        return simbolo.getValor() #RETORNAR EL VALOR DEL SIMBOLO ENCONTRADO