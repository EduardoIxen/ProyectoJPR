from os import pipe
from tkinter import *
from tkinter import Tk, Entry, Menu, messagebox, filedialog, ttk, Label, scrolledtext, INSERT, END, Button, Scrollbar, RIGHT, Y, HORIZONTAL, VERTICAL, simpledialog
from ui.Editor import ScrollText
from grammar import ejecutar


class MainWindow():
    def __init__(self):
        title = 'JPR EDITOR'
        self.fileName = ""
        self.root = Tk()
        self.root.title(title)
        self.root.state("zoomed")
        self.root.configure(bg = 'blue')

        #Menu bar
        menuBar = Menu(self.root)
        fileMenu = Menu(menuBar, tearoff=0)
        fileMenu.add_command(label="Crear Archivo", command = self.new_file)
        fileMenu.add_command(label="Abrir Archivo", command = self.open_file)
        fileMenu.add_command(label="Guardar", command = self.save_file)
        fileMenu.add_command(label="Guardar Como", command = self.saveAs_file)
        menuBar.add_cascade(label="Archivo", menu = fileMenu)

        reportMenu = Menu(menuBar, tearoff=0)
        reportMenu.add_command(label="Reporte De Errores", command = self.crearReporteErrores)
        reportMenu.add_command(label="Generar Arbol AST")
        reportMenu.add_command(label="Tabla De Símbolos")
        menuBar.add_cascade(label="Reportes", menu=reportMenu)
        self.root.config(menu=menuBar)

        #Botones correr y debug y label posicion
        self.textConsola = Entry(self.root, width=10)
        self.btnInterpretar = Button(self.root, text="Interpretar", bg='red', command=self.btn_run)
        self.btnDebug = Button(self.root, text="Debugger", bg='red')
        self.lblPos = Label(self.root, text="Línea:0 Columna:0")
        self.lblPos.pack()
        self.lblPos.place(x=600,y=570)

        #Creación de editores
        self.txt = ScrollText(self.root)
        self.txt.insert(END, '\n')
        self.txt.place(x=30, y=40)

        self.textConsola = scrolledtext.ScrolledText(self.root, width=70, height=32, bg="#cccccc", fg="#1a1a1a")
        self.textConsola.place(x=750, y=40)

        self.btnInterpretar.place(x=300, y=10)
        self.btnDebug.place(x=400, y=10)

        self.txt.text.bind("<ButtonRelease-1>", self.posicion)
        self.txt.text.bind("<KeyPress>", self.posicion)
        self.txt.text.bind("<Button-1>", self.posicion)


    def run(self):
        self.root.mainloop()


    def posicion(self, *args, **kwargs):
        posicion = self.txt.text.index(INSERT)
        posicion2 = posicion.split(".")
        self.lblPos.destroy()
        self.lblPos = Label(self.root, text=f"Línea: {posicion2[0]} Columna: {int(posicion2[1])+1}")
        self.lblPos.pack()
        self.lblPos.place(x=600,y=570)


    def new_file(self):
        self.fileName = ""
        self.txt.delete(1.0, END)
        self.textConsola.delete(1.0, END)

    def open_file(self):
        self.fileName = filedialog.askopenfilename(title= "Seleccionar archivo",initialdir = "./", filetypes= (("All Files", "*.*"), (".jpr", "*.jpr")))
        if self.fileName != "":
            file = open(self.fileName, "r")
            content = file.read()
            file.close()
            self.txt.delete("1.0", END)
            self.txt.insert("1.0", content)

    def saveAs_file(self):
        guardar = filedialog.asksaveasfilename(title = "Guardar Archivo", initialdir = "C:/", filetypes= (("Archivo jpr", "*.jpr"), ("rmt files", "*.rmt")))
        print("guaradasd ", guardar)
        fguardar = open(guardar, "w")
        fguardar.write(self.txt.get(1.0, END))
        fguardar.close()
        self.fileName = guardar

    def save_file(self):
        if self.fileName == "":
            guardar = filedialog.asksaveasfilename(title = "Guardar Archivo", initialdir="C:/", filetypes=((".jpr", "*.jpr"), ("rmt files", "*.rmt")))
            print("guaradasd ",guardar)
            fguardar = open(guardar, "w")
            fguardar.write(self.txt.get(1.0, END))
            fguardar.close()
            self.fileName = guardar
        else:
            file = open(self.fileName, "w")
            file.write(self.txt.get("1.0", END))
            file.close()


    def btn_run(self):
        from TS.Excepcion import listaErrores
        listaErrores.clear()
        entrada = ""
        entrada = self.txt.get("1.0", END)
        salidaConsola = ejecutar(entrada)
        self.textConsola.delete("1.0", END)
        self.textConsola.insert("1.0", salidaConsola)

    def crearReporteErrores(self):
        from Reporte.CrearReporteErrores import CrearReporteErrores
        CrearReporteErrores.crearReporteErrores(None)
