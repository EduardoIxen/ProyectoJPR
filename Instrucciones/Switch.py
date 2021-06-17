from tkinter.constants import NO
from Instrucciones.Break import Break
from TS.TablaSimbolos import TablaSimbolos
from TS.Excepcion import Excepcion
from Abstract.Instruccion import Instruccion

class Switch(Instruccion):
    def __init__(self, expresion, lsCase, instDefault, fila, columna):
        self.expresion = expresion
        self.lsCase = lsCase
        self.instDefault = instDefault
        self.fila = fila
        self.columna = columna
        
    def interpretar(self, tree, table):
        expresion = self.expresion.interpretar(tree, table)
        if isinstance(expresion, Excepcion): return expresion

        nuevaTabla = TablaSimbolos(table)

        #print("expresion->",expresion) #da 18
        #print("tipo 18->", self.expresion.tipo)
        #print("valor case->", caseSimple.condicion.interpretar(tree, nuevaTabla)) #valor varialbe en  case
        #print("case simple condi->",caseSimple.condicion.tipo) #tipo variable en case

        countMatch = 0
        countBreak = 0

        if self.lsCase != None:
            for caseSimple in self.lsCase:
                if caseSimple.condicion.tipo == self.expresion.tipo and \
                     caseSimple.condicion.interpretar(tree, nuevaTabla) == expresion:
                    countMatch = countMatch + 1
                    result = caseSimple.interpretar(tree, table)
                    if isinstance(result, Excepcion): return result
                    if isinstance(result, Break): 
                        countBreak = countBreak + 1
                        break

        if self.instDefault != None:
            if countBreak == 0:
                result = self.instDefault.interpretar(tree, nuevaTabla)
                if isinstance(result, Excepcion): return result
                if isinstance(result, Break): return
        


