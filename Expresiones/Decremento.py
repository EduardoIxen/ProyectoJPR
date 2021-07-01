from Abstract.NodoAST import NodoAST
from Abstract.Instruccion import Instruccion
from TS.Excepcion import Excepcion
from TS.Tipo import TIPO
from TS.Simbolo import Simbolo

class Decremento(Instruccion):
    def __init__(self, identificador, fila, columna):
        self.identificador = identificador
        self.fila = fila 
        self.columna = columna
        self.tipo = None

    def interpretar(self, tree, table):
        simbolo = table.getTabla(self.identificador.lower())  #obtener simbolo de la variable

        if simbolo == None:
            return Excepcion("Semantico", "Variable " + self.identificador + " no encontrada.", self.fila, self.columna)
        
        self.tipo = simbolo.getTipo()
        if self.tipo == TIPO.ENTERO or self.tipo == TIPO.DECIMAL: #DECREMENTO SOLO PARA DECIMALES Y ENTEROS
            valor = simbolo.getValor() - 1 #CAMBIO DE VALOR
            nuevoValor = Simbolo(self.identificador, self.tipo, self.fila, self.columna, valor)
            result = table.actualizarTabla(nuevoValor) #ACTUALIZAR EN LA TABLA DE SIMBOLOS

            if isinstance(valor, Excepcion): return result
            return nuevoValor.getValor()
        return Excepcion("Semantico", f"No se puede reducir variables de tipo {self.tipo}", self.fila, self.columna)

    def getNodo(self):
        nodo = NodoAST("DECREMENTO")
        nodo.agregarHijo(str(self.identificador))
        return nodo