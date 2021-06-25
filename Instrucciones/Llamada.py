from Instrucciones.Funcion import Funcion
from Abstract.Instruccion import Instruccion
from TS.TablaSimbolos import TablaSimbolos
from TS.Excepcion import Excepcion
from Instrucciones.Break import Break
from TS.Simbolo import Simbolo

class Llamada(Instruccion):
    def __init__(self, identificador, parametros, fila, columna):
        self.identificador = identificador
        self.parametros = parametros
        self.fila = fila
        self.columna = columna
    
    def interpretar(self, tree, table):
        result = tree.getFuncion(self.identificador.lower()) ##Obtener la funcion
        if result == None: #No se encontro la funcion
            return Excepcion("Semantico", "NO SE ENCONTRO LA FUNCION: "+self.identificador, self.fila, self.columna)

        nuevaTabla = TablaSimbolos(tree.getTSGlobal())

        #OBTENER PARAMETROS
        if len(result.parametros) == len(self.parametros): #verificar cantidad de parametros iguales
            contador = 0
            for expresion in self.parametros: #SE OBTIENE EL VALOR DEL PARAMETRO EN LA LLAMADA
                resultExpresion = expresion.interpretar(tree, table)
                if isinstance(resultExpresion, Excepcion): return resultExpresion

                if result.parametros[contador]['tipo'] == expresion.tipo: #VERIFICAR QUE SEAN DE TIPOS IGUALES
                    #CREACION DE SIMBOLOS E INGRESARLO A LA TABLA DE SIMBOLOS 
                    simbolo = Simbolo(str(result.parametros[contador]['identificador']), result.parametros[contador]['tipo'], self.fila, self.columna, resultExpresion)
                    resultTabla = nuevaTabla.setTabla(simbolo)
                    if isinstance(resultTabla, Excepcion): return resultTabla

                else:
                    return Excepcion("Semantico", "Tipo de dato diferente en parametros de la llamada.", self.fila, self.columna)
                contador += 1

            
        else: 
            return Excepcion("Semantico", "Cantidad de parametros incorrecta.", self.fila, self.columna)

        value = result.interpretar(tree, nuevaTabla) #Interpretar el nodo funcion
        if isinstance(value, Excepcion): return value
        self.tipo = result.tipo
        return value
