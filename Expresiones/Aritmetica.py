from re import T
from Abstract.Instruccion import Instruccion
from TS.Excepcion import Excepcion
from TS.Tipo import TIPO, OperadorAritmetico

class Aritmetica(Instruccion):
    def __init__(self, operador, OperacionIzq, OperacionDer, fila, columna):
        self.operador = operador
        self.OperacionIzq = OperacionIzq
        self.OperacionDer = OperacionDer
        self.fila = fila
        self.columna = columna
        self.tipo = None

    
    def interpretar(self, tree, table):
        izq = self.OperacionIzq.interpretar(tree, table)
        if isinstance(izq, Excepcion): return izq
        if self.OperacionDer != None:
            der = self.OperacionDer.interpretar(tree, table)
            if isinstance(der, Excepcion): return der


        if self.operador == OperadorAritmetico.MAS: ############################### SUMA ############################3
            if self.OperacionIzq.tipo == TIPO.ENTERO and self.OperacionDer.tipo == TIPO.ENTERO :
                self.tipo = TIPO.ENTERO
                return self.obtenerVal(self.OperacionIzq.tipo, izq) + self.obtenerVal(self.OperacionDer.tipo, der)
            elif self.OperacionIzq.tipo == TIPO.ENTERO and self.OperacionDer.tipo == TIPO.DECIMAL or self.OperacionIzq.tipo == TIPO.DECIMAL and self.OperacionDer.tipo == TIPO.ENTERO :
                self.tipo = TIPO.DECIMAL
                return self.obtenerVal(self.OperacionIzq.tipo, izq) + self.obtenerVal(self.OperacionDer.tipo, der)
            elif self.OperacionIzq.tipo == TIPO.ENTERO and self.OperacionDer.tipo == TIPO.BOOLEANO or self.OperacionIzq.tipo == TIPO.BOOLEANO and self.OperacionDer.tipo == TIPO.ENTERO:
                self.tipo = TIPO.ENTERO
                if izq == True:
                    return 1 + self.obtenerVal(self.OperacionDer.tipo, der)
                elif izq == False:
                    return (-1) + self.obtenerVal(self.OperacionDer.tipo, der)
                elif der == True:
                    return self.obtenerVal(self.OperacionIzq.tipo, izq) + 1
                elif der == False:
                    return self.obtenerVal(self.OperacionIzq.tipo, izq) + (-1)
            elif self.OperacionIzq.tipo == TIPO.ENTERO and self.OperacionDer.tipo == TIPO.CADENA or \
                self.OperacionIzq.tipo == TIPO.CADENA and self.OperacionDer.tipo == TIPO.ENTERO or \
                self.OperacionIzq.tipo == TIPO.DECIMAL and self.OperacionDer.tipo == TIPO.CADENA or \
                self.OperacionIzq.tipo == TIPO.CADENA and self.OperacionDer.tipo == TIPO.DECIMAL or\
                self.OperacionIzq.tipo == TIPO.BOOLEANO and self.OperacionDer.tipo == TIPO.CADENA or \
                self.OperacionIzq.tipo == TIPO.CADENA and self.OperacionDer.tipo == TIPO.BOOLEANO or \
                self.OperacionIzq.tipo == TIPO.CHARACTER and self.OperacionDer.tipo == TIPO.CADENA or \
                self.OperacionIzq.tipo == TIPO.CADENA and self.OperacionDer.tipo == TIPO.CHARACTER or \
                self.OperacionIzq.tipo == TIPO.CADENA and self.OperacionDer.tipo == TIPO.CADENA:
                self.tipo = TIPO.CADENA
                return str(self.obtenerVal(self.OperacionIzq.tipo, izq)) + str(self.obtenerVal(self.OperacionDer.tipo, der))
            elif self.OperacionIzq.tipo == TIPO.DECIMAL and self.OperacionDer.tipo == TIPO.DECIMAL:
                self.tipo = TIPO.DECIMAL
                return self.obtenerVal(self.OperacionIzq.tipo, izq) + self.obtenerVal(self.OperacionDer.tipo, der)
            elif self.OperacionIzq.tipo == TIPO.DECIMAL and self.OperacionDer.tipo == TIPO.BOOLEANO or \
                self.OperacionIzq.tipo == TIPO.BOOLEANO and self.OperacionDer.tipo == TIPO.DECIMAL:
                self.tipo = TIPO.DECIMAL
                if izq == True:
                    return 1 + self.obtenerVal(self.OperacionDer.tipo, der)
                elif izq == False:
                    return (-1) + self.obtenerVal(self.OperacionDer.tipo, der)
                elif der == True:
                    return self.obtenerVal(self.OperacionIzq.tipo, izq) + 1
                elif der == False:
                    return self.obtenerVal(self.OperacionIzq.tipo, izq) + (-1)
            elif self.OperacionIzq.tipo == TIPO.BOOLEANO and self.OperacionDer.tipo == TIPO.BOOLEANO:
                self.tipo = TIPO.ENTERO
                opDer = 0
                opIzq = 0
                opIzq = 1 if izq == True else opIzq -1
                opDer = 1 if der == True else opDer -1
                return opDer + opIzq
            elif self.OperacionIzq.tipo == TIPO.CHARACTER and self.OperacionDer.tipo == TIPO.CHARACTER:
                self.tipo = TIPO.CADENA
                return str(self.obtenerVal(self.OperacionIzq.tipo, izq)) + str(self.obtenerVal(self.OperacionDer.tipo, der))
            return Excepcion("Semantico", f"Error Semantico// No se pueden sumar los datos {str(izq)} ({self.OperacionIzq.tipo}) y {str(der)}({self.OperacionDer.tipo}).", self.fila, self.columna)

        elif self.operador == OperadorAritmetico.MENOS: #################################### RESTA ############################
            if self.OperacionIzq.tipo == TIPO.ENTERO and self.OperacionDer.tipo == TIPO.ENTERO:
                self.tipo = TIPO.ENTERO
                return self.obtenerVal(self.OperacionIzq.tipo, izq) - self.obtenerVal(self.OperacionDer.tipo, der)
            elif self.OperacionIzq.tipo == TIPO.ENTERO and self.OperacionDer.tipo == TIPO.DECIMAL or \
                self.OperacionIzq.tipo == TIPO.DECIMAL and self.OperacionDer.tipo == TIPO.ENTERO:
                self.tipo = TIPO.DECIMAL
                return self.obtenerVal(self.OperacionIzq.tipo, izq) - self.obtenerVal(self.OperacionDer.tipo, der)
            elif self.OperacionIzq.tipo == TIPO.ENTERO and self.OperacionDer.tipo == TIPO.BOOLEANO or \
                self.OperacionIzq.tipo == TIPO.BOOLEANO and self.OperacionDer.tipo == TIPO.ENTERO:
                self.tipo = TIPO.ENTERO
                if izq == True:
                    return 1 - self.obtenerVal(self.OperacionDer.tipo, der)
                elif izq == False:
                    return (-1) - self.obtenerVal(self.OperacionDer.tipo, der)
                elif der == True:
                    return self.obtenerVal(self.OperacionIzq.tipo, izq) - 1
                elif der == False:
                    return self.obtenerVal(self.OperacionIzq.tipo, izq) - (-1)
            elif self.OperacionIzq.tipo == TIPO.DECIMAL and self.OperacionDer.tipo == TIPO.DECIMAL:
                self.tipo = TIPO.DECIMAL
                return self.obtenerVal(self.OperacionIzq.tipo, izq) - self.obtenerVal(self.OperacionDer.tipo, der)
            elif self.OperacionIzq.tipo == TIPO.DECIMAL and self.OperacionDer.tipo == TIPO.BOOLEANO or \
                self.OperacionIzq.tipo == TIPO.BOOLEANO and self.OperacionDer.tipo == TIPO.DECIMAL:
                self.tipo = TIPO.DECIMAL
                if izq == True:
                    return 1 - self.obtenerVal(self.OperacionDer.tipo, der)
                elif izq == False:
                    return (-1) - self.obtenerVal(self.OperacionDer.tipo, der)
                elif der == True:
                    return self.obtenerVal(self.OperacionIzq.tipo, izq) - 1
                elif der == False:
                    return self.obtenerVal(self.OperacionIzq.tipo, izq) - (-1)
            return Excepcion("Semantico", f"No se pueden restar los datos {str(izq)} ({self.OperacionIzq.tipo}) y {str(der)}({self.OperacionDer.tipo}).", self.fila, self.columna)
        
        elif self.operador == OperadorAritmetico.POR: ############# MULTIPLICACION################
            if self.OperacionIzq.tipo == TIPO.ENTERO and self.OperacionDer.tipo == TIPO.ENTERO:
                self.tipo = TIPO.ENTERO
                return self.obtenerVal(self.OperacionIzq.tipo, izq) * self.obtenerVal(self.OperacionDer.tipo, der)
            elif self.OperacionIzq.tipo == TIPO.ENTERO and self.OperacionDer.tipo == TIPO.DECIMAL or \
                self.OperacionIzq.tipo == TIPO.DECIMAL and self.OperacionDer.tipo == TIPO.ENTERO:
                self.tipo = TIPO.DECIMAL
                return self.obtenerVal(self.OperacionIzq.tipo, izq) * self.obtenerVal(self.OperacionDer.tipo, der)
            elif self.OperacionIzq.tipo == TIPO.DECIMAL and self.OperacionDer.tipo == TIPO.DECIMAL:
                self.tipo = TIPO.DECIMAL
                return self.obtenerVal(self.OperacionIzq.tipo, izq) * self.obtenerVal(self.OperacionDer.tipo, der)
            return Excepcion("Semantico", f"No se puede multiplicar {str(izq)} ({self.OperacionIzq.tipo}) y {str(der)}({self.OperacionDer.tipo}).", self.fila, self.columna)

        elif self.operador == OperadorAritmetico.DIV: ############# DIVISION ################
            if self.obtenerVal(self.OperacionDer.tipo, der) == 0:
                    return Excepcion("Matematico", "Error matemático// Division por cero.", self.fila, self.columna)
            if self.OperacionIzq.tipo == TIPO.ENTERO and self.OperacionDer.tipo == TIPO.ENTERO:
                self.tipo = TIPO.DECIMAL
                return self.obtenerVal(self.OperacionIzq.tipo, izq) / self.obtenerVal(self.OperacionDer.tipo, der)
            elif self.OperacionIzq.tipo == TIPO.ENTERO and self.OperacionDer.tipo == TIPO.DECIMAL or \
                self.OperacionIzq.tipo == TIPO.DECIMAL and self.OperacionDer.tipo == TIPO.ENTERO:
                self.tipo = TIPO.DECIMAL
                return self.obtenerVal(self.OperacionIzq.tipo, izq) / self.obtenerVal(self.OperacionDer.tipo, der)
            elif self.OperacionIzq.tipo == TIPO.DECIMAL and self.OperacionDer.tipo == TIPO.DECIMAL:
                self.tipo = TIPO.DECIMAL
                return self.obtenerVal(self.OperacionIzq.tipo, izq) / self.obtenerVal(self.OperacionDer.tipo, der)
            return Excepcion("Semantico", f"No se puede dividir {str(izq)} ({self.OperacionIzq.tipo}) y {str(der)}({self.OperacionDer.tipo}).", self.fila, self.columna)
        
        elif self.operador == OperadorAritmetico.POT: ############# POTENCIA ##############
            if self.OperacionIzq.tipo == TIPO.ENTERO and self.OperacionDer.tipo == TIPO.ENTERO:
                self.tipo = TIPO.ENTERO
                return pow(self.obtenerVal(self.OperacionIzq.tipo, izq), self.obtenerVal(self.OperacionDer.tipo, der))
            elif self.OperacionIzq.tipo == TIPO.ENTERO and self.OperacionDer.tipo == TIPO.DECIMAL or \
                self.OperacionIzq.tipo == TIPO.DECIMAL and self.OperacionDer.tipo == TIPO.ENTERO:
                self.tipo = TIPO.DECIMAL
                return pow(self.obtenerVal(self.OperacionIzq.tipo, izq), self.obtenerVal(self.OperacionDer.tipo, der))
            elif self.OperacionIzq.tipo == TIPO.DECIMAL and self.OperacionDer.tipo == TIPO.DECIMAL:
                self.tipo = TIPO.DECIMAL
                return pow(self.obtenerVal(self.OperacionIzq.tipo, izq), self.obtenerVal(self.OperacionDer.tipo, der))
            return Excepcion("Semantico", f"Error al realizar la potenciaa {self.obtenerVal(self.OperacionIzq.tipo, izq)} ** {self.obtenerVal(self.OperacionDer.tipo, der)}", self.fila, self.columna)

        elif self.operador == OperadorAritmetico.MOD: ############# MODULO ##############
            if self.OperacionIzq.tipo == TIPO.ENTERO and self.OperacionDer.tipo == TIPO.ENTERO:
                self.tipo = TIPO.DECIMAL
                return self.obtenerVal(self.OperacionIzq.tipo, izq) % self.obtenerVal(self.OperacionDer.tipo, der)
            elif self.OperacionIzq.tipo == TIPO.ENTERO and self.OperacionDer.tipo == TIPO.DECIMAL or \
                self.OperacionIzq.tipo == TIPO.DECIMAL and self.OperacionDer.tipo == TIPO.ENTERO:
                self.tipo = TIPO.DECIMAL
                return self.obtenerVal(self.OperacionIzq.tipo, izq) % self.obtenerVal(self.OperacionDer.tipo, der)
            elif self.OperacionIzq.tipo == TIPO.DECIMAL and self.OperacionDer.tipo == TIPO.DECIMAL:
                self.tipo = TIPO.DECIMAL
                return self.obtenerVal(self.OperacionIzq.tipo, izq) % self.obtenerVal(self.OperacionDer.tipo, der)
            return Excepcion("Semantico", f"Error al realizar el módulo {self.obtenerVal(self.OperacionIzq.tipo, izq)} % {self.obtenerVal(self.OperacionDer.tipo, der)}", self.fila, self.columna)

        elif self.operador == OperadorAritmetico.UMENOS: ########### NEGACION ##########3
            if self.OperacionIzq.tipo == TIPO.ENTERO:
                self.tipo = TIPO.ENTERO
                return - self.obtenerVal(self.OperacionIzq.tipo, izq)
            elif self.OperacionIzq.tipo == TIPO.DECIMAL:
                self.tipo = TIPO.DECIMAL
                return - self.obtenerVal(self.OperacionIzq.tipo, izq)
            return Excepcion("Semantico", f"Tipo erroneo de dato para -.", self.fila, self.columna)
        return Excepcion("Semantico", f"Tipo de operacion no especificada.", self.fila, self.columna)

    def obtenerVal(self, tipo, val):
        if tipo == TIPO.ENTERO:
            return int(val)
        elif tipo == TIPO.DECIMAL:
            return float(val)
        elif tipo == TIPO.BOOLEANO:
            return bool(val)
        return str(val)