from TS.Excepcion import Excepcion
from TS.Tipo import TIPO
from TS.Tipo import OperadorAritmetico, OperadorRelacional, OperadorLogico

listaTablaSimbolos = []
class TablaSimbolos:
    def __init__(self, anterior = None):
        self.tabla = {} # Diccionario Vacio
        self.anterior = anterior

    def setTabla(self, simbolo):      # Agregar una variable a la tabla de símbolos
        if simbolo.id.lower() in self.tabla :
            return Excepcion("Semantico", "Variable " + simbolo.id + " ya existe", simbolo.fila, simbolo.columna)
        else:
            self.tabla[simbolo.id.lower()] = simbolo
            '''dic = {}
            dic['Identificador'] = simbolo.id.lower()
            dic['Tipo'] = self.formatGrafo(simbolo.getTipo())
            dic['Valor'] = simbolo.getValor()
            dic['Fila'] = simbolo.getFila()
            dic['Columna'] = simbolo.getColumna()

            agregarSimb = True
            for simb in listaTablaSimbolos:
                if simb.get("Identificador") == dic['Identificador'] and simb.get("Fila") == dic['Fila'] and \
                    simb.get("Columna") == dic['Columna']:
                    agregarSimb = False
            if agregarSimb:
                listaTablaSimbolos.append(dic)'''
            return None

    def getTabla(self, id):                     # obtener una variable de la tabla de simbolos por su id
        tablaActual = self
        while tablaActual != None:
            if id.lower() in tablaActual.tabla :
                return tablaActual.tabla[id.lower()]    #retorna el símbolo encontrado
            else:
                tablaActual = tablaActual.anterior
        return None

    '''
        # Actualizar el valor de un simbolo, buscando en la tabla de simbolos actual
        # y en las anteriores; comparando que el tipo anterior sea el mismo, Null ó
        # se le asigne valor null
    '''
    def actualizarTabla(self, simbolo):
        tablaActual = self
        while tablaActual != None:
            if simbolo.id.lower() in tablaActual.tabla :
                if tablaActual.tabla[simbolo.id.lower()].getTipo() == simbolo.getTipo() or \
                    simbolo.getTipo() == TIPO.NULO or tablaActual.tabla[simbolo.id.lower()].getTipo() == TIPO.NULO:
                    tablaActual.tabla[simbolo.id.lower()].setValor(simbolo.getValor())
                    tablaActual.tabla[simbolo.id.lower()].setTipo(simbolo.getTipo())
                    return None   ### VARIABLE ACTUALIZADA
                return Excepcion("Semantico", f"Tipo de dato diferente para la asignacion [{self.tabla[simbolo.id].getValor()} ({self.tabla[simbolo.id].getTipo()}) -> {simbolo.getValor()} ({simbolo.getTipo()})]", simbolo.getFila(), simbolo.getColumna())
            else:
                tablaActual = tablaActual.anterior
        return Excepcion("Semantico", f"Variable no encontrada en asignacion -{simbolo.id}-.", simbolo.getFila(), simbolo.getColumna())
        
    def formatGrafo(self, grafo):
        if grafo == TIPO.ENTERO:
            return "INT"
        elif grafo == TIPO.DECIMAL:
            return "DOUBLE"
        elif grafo == TIPO.BOOLEANO:
            return "BOOLEAN"
        elif grafo == TIPO.CHARACTER:
            return "CHAR"
        elif grafo == TIPO.CADENA:
            return "STRING"
        elif grafo == TIPO.NULO:
            return "NULL"
        elif grafo == TIPO.ARREGLO: 
            return "ARRAY"
        elif grafo == OperadorAritmetico.MAS:
            return "MAS"
        elif grafo == OperadorAritmetico.MENOS:
            return "MENOS"
        elif grafo == OperadorAritmetico.POR: 
            return "MULTIPLICACION"
        elif grafo == OperadorAritmetico.DIV:
            return "DIVISION"
        elif grafo == OperadorAritmetico.POT: 
            return "POTENCIA"
        elif grafo == OperadorAritmetico.MOD: 
            return "MODULO"
        elif grafo == OperadorAritmetico.UMENOS:
            return "NEGATIVO"
        elif grafo == OperadorRelacional.MENORQUE: 
            return "MENOR QUE"
        elif grafo == OperadorRelacional.MAYORQUE: 
            return "MAYOR QUE"
        elif grafo == OperadorRelacional.MENORIGUAL:
            return "MENOR IGUAL"
        elif grafo == OperadorRelacional.MAYORIGUAL: 
            return "MAYOR IGUAL"
        elif grafo == OperadorRelacional.IGUALIGUAL: 
            return "IGUAL IGUAL"
        elif grafo == OperadorRelacional.DIFERENTE: 
            return "DIFERENTE"
        elif grafo == OperadorLogico.AND: 
            return "AND"
        elif grafo == OperadorLogico.OR: 
            return "OR"
        elif grafo == OperadorLogico.NOT: 
            return "NOT"
        return grafo