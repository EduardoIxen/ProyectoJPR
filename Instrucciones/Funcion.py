from Instrucciones.Continue import Continue
from Instrucciones.Return import Return
from Abstract.Instruccion import Instruccion
from TS.TablaSimbolos import TablaSimbolos
from TS.Excepcion import Excepcion
from Instrucciones.Break import Break
from TS.Tipo import TIPO

class Funcion(Instruccion):
    def __init__(self, identificador, parametros, instrucciones, fila, columna):
        self.identificador = identificador.lower()
        self.parametros = parametros
        self.instrucciones = instrucciones
        self.fila = fila
        self.columna = columna
        self.tipo = TIPO.NULO
    
    def interpretar(self, tree, table):
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
            if isinstance(value, Return):
                self.tipo = value.tipo
                return value.result
            if isinstance(value, Continue):
                err = Excepcion("Semantico", "Sentencia CONTINUE fuera de ciclo.", instruccion.fila, instruccion.columna)
                tree.getExcepciones().append(err) #Guardar el error
                tree.updateConsola(err.toString())
        return None
