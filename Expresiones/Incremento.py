from Abstract.NodoAST import NodoAST
from TS.Tipo import TIPO
from tkinter.constants import NO
from Abstract.Instruccion import Instruccion
from TS.Simbolo import Simbolo
from TS.Excepcion import Excepcion


class Incremento(Instruccion):
    def __init__(self, identificador, fila, columna):
        self.identificador = identificador
        self.fila = fila
        self.columna = columna
        self.tipo = None

    def interpretar(self, tree, table):
        simbolo = table.getTabla(self.identificador.lower()) #OBTENER SIMBOLO DEL ATABLA DE SIMBOLO MEDIANTE ID

        if simbolo == None:
            return Excepcion("Semantico", "Variable " + self.identificador + " no encontrada.", self.fila, self.columna)

        self.tipo = simbolo.getTipo()
        if self.tipo == TIPO.ENTERO or self.tipo == TIPO.DECIMAL: #INCREMENTO PARA DECIMALES Y ENTEROS
            valor = simbolo.getValor() + 1
            nuevoValor = Simbolo(self.identificador, self.tipo, False, self.fila, self.columna, valor)
            result = table.actualizarTabla(nuevoValor) #ACTUALIAR EN TABLA DE SIMBOLOS

            if isinstance(valor, Excepcion): return result
            return nuevoValor.getValor()
        return Excepcion("Semantico", f"No se puede incrementar variables de tipo {self.tipo}", self.fila, self.columna)

    def getNodo(self):
        nodo = NodoAST("INCREMENTO")
        nodo.agregarHijo(str(self.identificador))
        return nodo