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
        
        USER_INP = simpledialog.askstring(title="Test", prompt="What's your Name?:")

        return USER_INP  #retornar el valor(obtenido en la gramatica) del dato primitivo
