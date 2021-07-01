from Abstract.NodoAST import NodoAST
from Abstract.Instruccion import Instruccion
from TS.Excepcion import Excepcion
from TS.Tipo import TIPO, OperadorLogico

class Logica(Instruccion):
    def __init__(self, operador, OperacionIzq, OperacionDer, fila, columna):
        self.operador = operador
        self.OperacionIzq = OperacionIzq
        self.OperacionDer = OperacionDer
        self.fila = fila
        self.columna = columna
        self.tipo = TIPO.BOOLEANO
    
    def interpretar(self, tree, table):
        izq = self.OperacionIzq.interpretar(tree, table)
        if isinstance(izq, Excepcion): return izq
        if self.OperacionDer != None:
            der = self.OperacionDer.interpretar(tree, table)
            if isinstance(der, Excepcion): return der
        
        if self.operador == OperadorLogico.AND: ########################## && ################################
            if self.OperacionIzq.tipo == TIPO.BOOLEANO and self.OperacionDer.tipo == TIPO.BOOLEANO:
                return self.obtenerVal(self.OperacionIzq.tipo, izq) and self.obtenerVal(self.OperacionDer.tipo, der)
            return Excepcion("Semantico", f"Tipo Erroneo de operacion {str(izq)} ({self.OperacionIzq.tipo}) && {str(der)}({self.OperacionDer.tipo}).", self.fila, self.columna)
        elif self.operador == OperadorLogico.OR: ####################### || #################################
            if self.OperacionIzq.tipo == TIPO.BOOLEANO and self.OperacionDer.tipo == TIPO.BOOLEANO:
                return self.obtenerVal(self.OperacionIzq.tipo, izq) or self.obtenerVal(self.OperacionDer.tipo, der)
            return Excepcion("Semantico", f"Tipo Erroneo de operacion {str(izq)} ({self.OperacionIzq.tipo}) || {str(der)}({self.OperacionDer.tipo}).", self.fila, self.columna)
        elif self.operador == OperadorLogico.NOT: ##################### ! ###################################
            if self.OperacionIzq.tipo == TIPO.BOOLEANO:
                return not self.obtenerVal(self.OperacionIzq.tipo, izq)
            return Excepcion("Semantico", f"Tipo Erroneo de operacion ! {str(izq)} ({self.OperacionIzq.tipo}).", self.fila, self.columna)

    def getNodo(self):
        nodo = NodoAST("LOGICA")
        if self.OperacionDer != None:
            nodo.agregarHijoNodo(self.OperacionIzq.getNodo())
            nodo.agregarHijo(str(self.operador))
            nodo.agregarHijoNodo(self.OperacionDer.getNodo())
        else:
            nodo.agregarHijo(str(self.operador))
            nodo.agregarHijoNodo(self.OperacionIzq.getNodo())
        
        return nodo

    def obtenerVal(self, tipo, val):
        if tipo == TIPO.ENTERO:
            return int(val)
        elif tipo == TIPO.DECIMAL:
            return float(val)
        elif tipo == TIPO.BOOLEANO:
            return bool(val)
        return str(val)
