from Abstract.NodoAST import NodoAST
from Abstract.Instruccion import Instruccion
from TS.Tipo import TIPO
from tkinter import *
from tkinter import simpledialog
import sys

class Read(Instruccion):
    def __init__(self, fila, columna):
        self.fila = fila
        self.columna = columna
        self.tipo = TIPO.CADENA

    def interpretar(self, tree, table):
        tree.getTxtConsola().delete("1.0", END)
        tree.getTxtConsola().insert("1.0", tree.getConsola())
        #tree.setConsola("")
        
        USER_INP = simpledialog.askstring(title="Read", prompt="Ingrese el dato solicitado.")
        tree.updateConsola("->"+USER_INP)
        tree.getTxtConsola().delete("1.0", END)
        tree.getTxtConsola().insert("1.0", tree.getConsola())

        return USER_INP  #retornar el valor(obtenido en la gramatica) del dato primitivo

    def getNodo(self):
        nodo = NodoAST("READ")
        return nodo