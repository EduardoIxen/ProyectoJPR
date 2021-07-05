
from Instrucciones.DeclaracionReferencia import DeclaracionReferencia
from Instrucciones.DeclaracionArr1 import DeclaracionArr1
from Instrucciones.Declaracion import Declaracion
from Abstract.NodoAST import NodoAST
from Instrucciones.Continue import Continue
from Instrucciones.Return import Return
from Abstract.Instruccion import Instruccion
from TS.Excepcion import Excepcion
from TS.TablaSimbolos import TablaSimbolos
from TS.Tipo import TIPO
from Instrucciones.Break import Break

class While(Instruccion):
    def __init__(self, condicion, instrucciones, fila, columna):
        self.condicion = condicion
        self.instrucciones = instrucciones
        self.fila = fila
        self.columna = columna
        self.tabla = None

    def interpretar(self, tree, table):
        self.tabla = table
        while True:
            condicion = self.condicion.interpretar(tree, table)
            if isinstance(condicion, Excepcion): return condicion

            if self.condicion.tipo == TIPO.BOOLEANO:
                if bool(condicion) == True:   # VERIFICA SI ES VERDADERA LA CONDICION
                    nuevaTabla = TablaSimbolos(table)       #NUEVO ENTORNO para cada ciclo
                    for instruccion in self.instrucciones:
                        result = instruccion.interpretar(tree, nuevaTabla) #EJECUTA INSTRUCCION ADENTRO DEL while
                        if isinstance(result, Excepcion) :
                            tree.getExcepciones().append(result)
                            tree.updateConsola(result.toString())
                        if isinstance(result, Break):
                            return None
                        if isinstance(result, Return): return result
                        if isinstance(result, Continue): break #dejar de ejecutar las instrucciones del ciclo actual del while y pasar al siguiente ciclo
                else:
                    break
            else:
                return Excepcion("Semantico", "Tipo de dato no booleano en while.", self.fila, self.columna)

    def getNodo(self):
        nodo = NodoAST("WHILE")

        instruccionesIf = NodoAST("INSTRUCCIONES")
        for instr in self.instrucciones:
            instruccionesIf.agregarHijoNodo(instr.getNodo())
        nodo.agregarHijoNodo(instruccionesIf)

        return nodo

    def getTabla(self,tree,table, padre):
        from TS.TablaSimbolos import listaTablaSimbolos
        salida = ""
        #salida += "-¿¿¿Funcion¿¿¿" + nombre + "¿¿¿"+ nombreFunc  + "¿¿¿" + str(self.fila) + "¿¿¿"+ str(self.columna)+ "¿¿¿ - &&\n"
        for instr in self.instrucciones:
            if isinstance(instr, Declaracion) :
                salida += str(instr.getTabla(tree,self.tabla, padre))
            if (isinstance(instr, DeclaracionArr1)):
                salida += instr.getTabla(tree,table, padre)
            if (isinstance(instr, DeclaracionReferencia)):
                salida += instr.getTabla(tree,table, padre)

        
        return salida