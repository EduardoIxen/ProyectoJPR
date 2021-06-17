from TS.TablaSimbolos import TablaSimbolos
from TS.Tipo import TIPO
from Abstract.Instruccion import Instruccion
from TS.Excepcion import Excepcion
from Instrucciones.Break import Break


class Case(Instruccion):
    def __init__(self, condicion, instrucciones, fila, columna):
        self.condicion = condicion
        self.instrucciones = instrucciones
        self.fila = fila
        self.columna = columna

    def interpretar(self, tree, table):
        nuevaTabla = TablaSimbolos(table)
        for instruccion in self.instrucciones:
            result = instruccion.interpretar(tree, nuevaTabla)
            if isinstance(result, Excepcion):
                tree.getExcepciones().append(result)
                tree.updateConsola(result.toString())
            if isinstance(result, Break): return result
        
        return None

