from TS.Tipo import TIPO
from Abstract.NodoAST import NodoAST
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

                if self.identificador.lower() == "typeof":
                    result.parametros[contador]['tipo'] = expresion.tipo  #igualar el tipo de la expresion recibida con el tipo del parametro de la funcion nativa
                if self.identificador.lower() == "length":
                    result.parametros[contador]['tipo'] = expresion.tipo

                #print("result tipo",result.parametros[contador]['tipo'])
                #print("tipo arre:", result.parametros[contador]['tipoArreglo'])

                #print("exp tip",expresion.tipo)
                #print("resul expr->", resultExpresion)

                if result.parametros[contador]['tipo'] == expresion.tipo or self.identificador.lower() == "truncate" \
                    or self.identificador.lower() == "round" or self.identificador.lower() == "typeof" : #VERIFICAR QUE SEAN DE TIPOS IGUALES
                    #CREACION DE SIMBOLOS E INGRESARLO A LA TABLA DE SIMBOLOS 
                    simbolo = Simbolo(str(result.parametros[contador]['identificador']).lower(), result.parametros[contador]['tipo'], False, self.fila, self.columna, resultExpresion)
                    resultTabla = nuevaTabla.setTabla(simbolo)
                    if isinstance(resultTabla, Excepcion): return resultTabla
                elif (result.parametros[contador]['tipo'] == TIPO.ARREGLO and isinstance(resultExpresion, list)):
                    print("si es arreglo")
                    if (result.parametros[contador]['tipoArreglo'] == expresion.tipo):
                        print("mismo tipo dato")
                        simbolo = Simbolo(str(result.parametros[contador]['identificador']).lower(), result.parametros[contador]['tipoArreglo'], True, self.fila, self.columna, resultExpresion)
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

    def getNodo(self):
        nodo = NodoAST("LLAMADA A FUNCION")
        nodo.agregarHijo(str(self.identificador))
        parametros = NodoAST("PARAMETROS")
        for param in self.parametros:
            parametros.agregarHijoNodo(param.getNodo())
        nodo.agregarHijoNodo(parametros)

        '''if self.identificador.lower() != "typeof" and self.identificador.lower() != "length" and\
            self.identificador.lower() != "round" and self.identificador.lower() != "tolower" and\
            self.identificador.lower() != "toupper" and self.identificador.lower() != "truncate":
            instrucciones = NodoAST("INSTRUCCIONES")
            for instr in self.instrucciones:
                instrucciones.agregarHijoNodo(instr.getNodo())
            nodo.agregarHijoNodo(instrucciones)
        '''
        return nodo