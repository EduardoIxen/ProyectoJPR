class NodoAST():
    def __init__(self, valor):
        self.hijos = []
        self.valor = valor

    def setHijos(self, hijos):
         self.hijos = hijos

    def agregarHijo(self, valorHijo):
        self.hijos.append(NodoAST(self.formatGrafo(str(valorHijo))))

    def agregarHijos(self, hijos):
        for hijo in hijos:
            self.hijos.append(hijo)

    def agregarHijoNodo(self, hijo):
        self.hijos.append(hijo)

    def agregarPrimerHijo(self, valorHijo):
        self.hijos.insert(0, NodoAST(valorHijo))

    def agregarPrimerHijoNodo(self, hijo):
        self.hijos.insert(0, hijo)

    def getValor(self):
        return str(self.valor)

    def setValor(self, valor):
        self.valor = valor
    
    def getHijos(self):
        return self.hijos
    
    def formatGrafo(self, grafo):
        if grafo == "TIPO.ENTERO":
            return "INT"
        elif grafo == "TIPO.DECIMAL":
            return "DOUBLE"
        elif grafo == "TIPO.BOOLEANO":
            return "BOOLEAN"
        elif grafo == "TIPO.CHARACTER":
            return "CHAR"
        elif grafo == "TIPO.CADENA":
            return "STRING"
        elif grafo == "TIPO.NULO":
            return "NULL"
        elif grafo == "TIPO.ARREGLO": 
            return "ARRAY"
        elif grafo == "OperadorAritmetico.MAS":
            return "MAS"
        elif grafo == "OperadorAritmetico.MENOS":
            return "MENOS"
        elif grafo == "OperadorAritmetico.POR": 
            return "MULTIPLICACION"
        elif grafo == "OperadorAritmetico.DIV":
            return "DIVISION"
        elif grafo == "OperadorAritmetico.POT": 
            return "POTENCIA"
        elif grafo == "OperadorAritmetico.MOD": 
            return "MODULO"
        elif grafo == "OperadorAritmetico.UMENOS":
            return "NEGATIVO"
        elif grafo == "OperadorRelacional.MENORQUE": 
            return "MENOR QUE"
        elif grafo == "OperadorRelacional.MAYORQUE": 
            return "MAYOR QUE"
        elif grafo == "OperadorRelacional.MENORIGUAL":
            return "MENOR IGUAL"
        elif grafo == "OperadorRelacional.MAYORIGUAL": 
            return "MAYOR IGUAL"
        elif grafo == "OperadorRelacional.IGUALIGUAL": 
            return "IGUAL IGUAL"
        elif grafo == "OperadorRelacional.DIFERENTE": 
            return "DIFERENTE"
        elif grafo == "OperadorLogico.AND": 
            return "AND"
        elif grafo == "OperadorLogico.OR": 
            return "OR"
        elif grafo == "OperadorLogico.NOT": 
            return "NOT"
        return grafo