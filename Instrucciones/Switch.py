from Instrucciones.DeclaracionArr1 import DeclaracionArr1
from Instrucciones.Declaracion import Declaracion
from Instrucciones.Case import Case
from Abstract.NodoAST import NodoAST
from Instrucciones.Continue import Continue
from Instrucciones.Return import Return
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
        self.tabla = None
        
    def interpretar(self, tree, table):
        self.tabla = table
        expresion = self.expresion.interpretar(tree, table) #Obtener el valor de la expresion del switch
        if isinstance(expresion, Excepcion): return expresion

        nuevaTabla = TablaSimbolos(table)

        '''
            RECORRER LA LISTA DE CASE Y LUEGO COMPARAR QUE EL TIPO DE LA EXPRESION EN EL
            SWITCH SEA EL MISMO QUE EL DE LA EXPRESION EN EL CASE Y TAMBIEN COMPARAR EL
            VALOR DE CADA EXPRESION.

            SI SE CUMPLE, INTERPRETAR EL CASE (EJECUTA CADA INSTRUCCION DENTRO ) -> CASE.PY

            SI ENCUENTRA UN BREAK DENTRO DE UN CASE, YA NO SIGUE RECORRIENDO LA LISTA DE CASE

            SI NO HAY NINGUN BREAK EJECUTA EL DEAFULT, SI HUBIESE UNO
        '''

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
                    if isinstance(result, Return): return result
                    if isinstance(result, Continue): return result #retornar instancia de continue para marcar error

        if self.instDefault != None:
            if countBreak == 0:
                result = self.instDefault.interpretar(tree, nuevaTabla)
                if isinstance(result, Excepcion): return result
                if isinstance(result, Break): return
                if isinstance(result, Return): return result
                if isinstance(result, Continue): return result  #retornar instancia de continue para marcar error
        

    def getNodo(self):
        nodo = NodoAST("SWITCH")
        lsCase = NodoAST("LISTA CASE")
        for caso in self.lsCase:
            lsCase.agregarHijoNodo(caso.getNodo())
        nodo.agregarHijoNodo(lsCase)
        
        if self.instDefault != None:
            defaultIns = NodoAST("DEFAULT")    
            defaultIns.agregarHijoNodo(self.instDefault.getNodo())
            nodo.agregarHijoNodo(defaultIns)
        
        return nodo

    def getTabla(self,tree,table, padre):
        from TS.TablaSimbolos import listaTablaSimbolos
        salida = ""
        #salida += "-??????Funcion??????" + nombre + "??????"+ nombreFunc  + "??????" + str(self.fila) + "??????"+ str(self.columna)+ "?????? - &&\n"
        for instr in self.lsCase:
            if isinstance(instr, Case) :
                salida += str(instr.getTabla(tree,self.tabla, padre))

        if self.instDefault != None:
            if isinstance(self.instDefault, Case):
                self.instDefault.getTabla(tree, self.tabla, padre)
                    
        return salida