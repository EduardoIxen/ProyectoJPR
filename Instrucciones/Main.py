from Instrucciones.Case import Case
from Instrucciones.DeclaracionArr1 import DeclaracionArr1
from Instrucciones.While import While
from Instrucciones.For import For
from Instrucciones.If import If
from Instrucciones.Switch import Switch
from Instrucciones.Declaracion import Declaracion
from Abstract.NodoAST import NodoAST
from Instrucciones.Continue import Continue
from Abstract.Instruccion import Instruccion
from TS.TablaSimbolos import TablaSimbolos
from TS.Excepcion import Excepcion
from Instrucciones.Break import Break

class Main(Instruccion):
    def __init__(self, instrucciones, fila, columna):
        self.instrucciones = instrucciones
        self.fila = fila
        self.columna = columna
        self.tabla = None
        self.identificador = "Main"
    
    def interpretar(self, tree, table):
        self.tabla = table
        nuevaTabla = TablaSimbolos(table) 
        for instruccion in self.instrucciones:      # RECORRE TODAS LAS INSTRUCCIOES QUE TIENE DENTRO
            value = instruccion.interpretar(tree,nuevaTabla) #EJECUTA CADA INSTRUCCION
            if isinstance(value, Excepcion) :
                tree.getExcepciones().append(value)
                tree.updateConsola(value.toString())
            if isinstance(value, Break): 
                err = Excepcion("Semantico", "Sentencia BREAK fuera de ciclo", instruccion.fila, instruccion.columna)
                tree.getExcepciones().append(err) #GUARDA EL ERROR PARA SEGUIR CON LAS DEMAS INSTRUCCIONES
                tree.updateConsola(err.toString())
            if isinstance(value, Continue):
                err = Excepcion("Semantico", "Sentencia CONTINUE fuera de ciclo.", instruccion.fila, instruccion.columna)
                tree.getExcepciones().append(err)
                tree.updateConsola(err.toString())

    def getNodo(self):
        nodo = NodoAST("MAIN")

        instruccionesIf = NodoAST("INSTRUCCIONES")
        for instr in self.instrucciones:
            instruccionesIf.agregarHijoNodo(instr.getNodo())
        nodo.agregarHijoNodo(instruccionesIf)

        return nodo

    def getTabla(self,tree,table, padre):
        from TS.TablaSimbolos import listaTablaSimbolos
        salida = ""
        nombre = "Main"
        nombreFunc = "Funcion"

        salida += "-¿¿¿Funcion¿¿¿" + nombre + "¿¿¿"+ nombreFunc  + "¿¿¿" + str(self.fila) + "¿¿¿"+ str(self.columna)+ "¿¿¿ - &&\n"
        for instr in self.instrucciones:
            if isinstance(instr, Declaracion) :
                salida += str(instr.getTabla(tree,self.tabla,"Main"))
            if isinstance(instr, If):
                salida += str(instr.getTabla(tree,table,"Main" + " -> If"))
            if isinstance(instr, For):
                salida += str(instr.getTabla(tree,table,"Main"+" -> For"))
            if isinstance(instr, While):
                salida += str(instr.getTabla(tree,table,"Main"+" -> While"))
            if (isinstance(instr, DeclaracionArr1)):
                salida += instr.getTabla(tree,table,"Main")
            if (isinstance(instr, Switch)):
                salida += instr.getTabla(tree, table, "Main->Switch")

        dic = {}
        dic['Identificador'] = str(self.identificador)
        dic['Tipo'] = "Funcion Principal"
        dic['Tipo2'] = "-----"
        dic['Entorno'] = str(padre)
        dic['Valor'] = "-----"
        dic['Fila'] = str(self.fila)
        dic['Columna'] = str(self.columna)
        
        listaTablaSimbolos.append(dic)
        
        return salida