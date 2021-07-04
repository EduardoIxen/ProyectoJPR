
from Instrucciones.DeclaracionArr1 import DeclaracionArr1
from Instrucciones.While import While
from Instrucciones.For import For
from Instrucciones.Declaracion import Declaracion
from Abstract.NodoAST import NodoAST
from Instrucciones.Continue import Continue
from Instrucciones.Return import Return
from Abstract.Instruccion import Instruccion
from TS.Excepcion import Excepcion
from TS.Tipo import TIPO
from TS.TablaSimbolos import TablaSimbolos
from Instrucciones.Break import Break

class If(Instruccion):
    def __init__(self, condicion, instruccionesIf, instruccionesElse, ElseIf, fila, columna):
        self.condicion = condicion
        self.instruccionesIf = instruccionesIf
        self.instruccionesElse = instruccionesElse
        self.elseIf = ElseIf
        self.fila = fila
        self.columna = columna
        self.tabla = None

    def interpretar(self, tree, table):
        self.tabla = table
        condicion = self.condicion.interpretar(tree, table)
        if isinstance(condicion, Excepcion): return condicion

        if self.condicion.tipo == TIPO.BOOLEANO:
            if bool(condicion) == True:   # VERIFICA SI ES VERDADERA LA CONDICION
                nuevaTabla = TablaSimbolos(table)       #NUEVO ENTORNO
                for instruccion in self.instruccionesIf:
                    result = instruccion.interpretar(tree, nuevaTabla) #EJECUTA INSTRUCCION ADENTRO DEL IF
                    if isinstance(result, Excepcion) :
                        tree.getExcepciones().append(result)
                        tree.updateConsola(result.toString())
                    if isinstance(result, Break): return result
                    if isinstance(result, Return): return result
                    if isinstance(result, Continue): return result #Retornar instancia de continue para marcar error
            else:               #ELSE
                if self.instruccionesElse != None:
                    nuevaTabla = TablaSimbolos(table)       #NUEVO ENTORNO
                    for instruccion in self.instruccionesElse:
                        result = instruccion.interpretar(tree, nuevaTabla) #EJECUTA INSTRUCCION ADENTRO DEL ELSE
                        if isinstance(result, Excepcion) :
                            tree.getExcepciones().append(result)
                            tree.updateConsola(result.toString()) 
                        if isinstance(result, Break): return result
                        if isinstance(result, Return): return result
                        if isinstance(result, Continue): return result #Retornar instancia de continue para marcar error
                elif self.elseIf != None:
                    result = self.elseIf.interpretar(tree, table)  #SI ES ELSE-IF vuelve al inicio como un nuevo if y evalua denuevo
                    if isinstance(result, Excepcion): return result
                    if isinstance(result, Break): return result
                    if isinstance(result, Return): return result
                    if isinstance(result, Continue): return result  #Retornar instancia de continue para marcar error
        else:
            return Excepcion("Semantico", "Condicion invalida en if.", self.fila, self.columna)

    
    def getNodo(self):
        nodo = NodoAST("IF")

        instruccionesIf = NodoAST("INSTRUCCIONES")
        for instr in self.instruccionesIf:
            instruccionesIf.agregarHijoNodo(instr.getNodo())
        nodo.agregarHijoNodo(instruccionesIf)

        if self.instruccionesElse != None:
            instruccionesElse = NodoAST("INSTRUCCIONES")
            for instr in self.instruccionesElse:
                instruccionesElse.agregarHijoNodo(instr.getNodo())
            nodo.agregarHijoNodo(instruccionesElse)
        elif self.elseIf != None:
            nodo.agregarHijoNodo(self.elseIf.getNodo())

        return nodo

    def getTabla(self,tree,table, padre):
        from TS.TablaSimbolos import listaTablaSimbolos
        salida = ""
        #salida += "-¿¿¿Funcion¿¿¿" + nombre + "¿¿¿"+ nombreFunc  + "¿¿¿" + str(self.fila) + "¿¿¿"+ str(self.columna)+ "¿¿¿ - &&\n"
        for instr in self.instruccionesIf:
            if isinstance(instr, Declaracion) :
                salida += str(instr.getTabla(tree,self.tabla, padre))
            if (isinstance(instr, DeclaracionArr1)):
                salida += instr.getTabla(tree,table, padre)

        if self.instruccionesElse != None:
            for instr in self.instruccionesElse:
                if isinstance(instr, Declaracion) :
                    salida += str(instr.getTabla(tree,self.tabla, padre))
                if (isinstance(instr, DeclaracionArr1)):
                    salida += instr.getTabla(tree,table, padre)
        
        if self.elseIf != None:
            if isinstance(self.elseIf, If):
                self.elseIf.getTabla(tree, table, padre)

        
        return salida