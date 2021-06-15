import webbrowser
import os.path
from tabulate import *

listaErrores = []
class Excepcion:
    def __init__(self, tipo, descripcion, fila, columna):
        self.tipo = tipo
        self.descripcion = descripcion
        self.fila = fila
        self.columna = columna

    def toString(self):
        dicError = {}
        dicError["Tipo"] = self.tipo
        dicError["Descripcion"] = self.descripcion
        dicError["Fila"] = self.fila
        dicError["Columna"] = self.columna
        listaErrores.append(dicError)
        return self.tipo + " - " + self.descripcion + " [" + str(self.fila) + "," + str(self.columna) + "]"
