from tkinter.constants import N
from TS.Tipo import TIPO
from Abstract.Instruccion import Instruccion
from TS.TablaSimbolos import TablaSimbolos
from TS.Excepcion import Excepcion
from Instrucciones.Break import Break


class For(Instruccion):
    def __init__(self, declasignacion, condicion, actualizacion, instrucciones, fila, columna):
        self.declasignacion = declasignacion
        self.condicion = condicion
        self.actualizacion = actualizacion
        self.instrucciones = instrucciones
        self.fila = fila
        self.columna = columna

    def interpretar(self, tree, table):
        nuevaTabla = TablaSimbolos(table)  # NUEVO ENTORNO
        if self.declasignacion != None:
            declasigna = self.declasignacion.interpretar(tree, nuevaTabla)  # asignacion de nueva variable
            if isinstance(declasigna, Excepcion):
                return declasigna

        # realizar la operacion de comparacion
        condicion = self.condicion.interpretar(tree, nuevaTabla)
        if isinstance(condicion, Excepcion):
            return condicion

        if self.condicion.tipo != TIPO.BOOLEANO:
            return Excepcion("Semantico", "Tipo de dato no booleano en condicion.", self.fila, self.columna)

        while bool(condicion) == True:
            nuevaTabla2 = TablaSimbolos(nuevaTabla)       #NUEVO ENTORNO
            for instruccion in self.instrucciones:
                result = instruccion.interpretar(tree, nuevaTabla2)
                if isinstance(result, Excepcion):
                    tree.getExcepciones().append(result)
                    tree.updateConsola(result.toString())
                if isinstance(result, Break):
                    return None

            if self.actualizacion != None:
                actualizacion = self.actualizacion.interpretar(
                    tree, nuevaTabla2)
                if isinstance(actualizacion, Excepcion):
                    return actualizacion

            # realizar la operacion de comparacion
            condicion = self.condicion.interpretar(tree, nuevaTabla2)
            if isinstance(condicion, Excepcion):
                return condicion

            if self.condicion.tipo != TIPO.BOOLEANO:
                return Excepcion("Semantico", "Tipo de dato no booleano en condicion.", self.fila, self.columna)