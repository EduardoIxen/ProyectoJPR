from Abstract.NodoAST import NodoAST
from Instrucciones.Continue import Continue
from Instrucciones.Return import Return
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

    '''
        Cuando se ejecuta el interpretar de un case, se ejecutan todas las
        instrucciones que posea creando una nueva tabla de simbolos para 
        cada case.
    '''
    def interpretar(self, tree, table):
        nuevaTabla = TablaSimbolos(table)
        for instruccion in self.instrucciones:
            result = instruccion.interpretar(tree, nuevaTabla)
            if isinstance(result, Excepcion):
                tree.getExcepciones().append(result)
                tree.updateConsola(result.toString())
            if isinstance(result, Break): return result
            if isinstance(result, Return): return result
            if isinstance(result, Continue): return result  #retornar instancia de CONTINUE para marcar error
        
        return None

    def getNodo(self):
        nodo = NodoAST("CASE")
        instrucciones = NodoAST("INSTRUCCIONES")
        for instr in self.instrucciones:
            instrucciones.agregarHijoNodo(instr.getNodo())
        nodo.agregarHijoNodo(instrucciones)
        return nodo