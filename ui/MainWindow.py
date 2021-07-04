import re
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
        self.root.configure(bg='blue')

        ################################# MENU BAR ##################################
        menuBar = Menu(self.root)
        fileMenu = Menu(menuBar, tearoff=0)
        fileMenu.add_command(label="Crear Archivo", command=self.new_file)
        fileMenu.add_command(label="Abrir Archivo", command=self.open_file)
        fileMenu.add_command(label="Guardar", command=self.save_file)
        fileMenu.add_command(label="Guardar Como", command=self.saveAs_file)
        menuBar.add_cascade(label="Archivo", menu=fileMenu)

        reportMenu = Menu(menuBar, tearoff=0)
        reportMenu.add_command(label="Reporte De Errores", command=self.crearReporteErrores)
        reportMenu.add_command(label="Generar Arbol AST", command=self.crearAST)
        reportMenu.add_command(label="Tabla De Símbolos", command=self.crearReporteTS)
        menuBar.add_cascade(label="Reportes", menu=reportMenu)
        self.root.config(menu=menuBar)

        #################### BOTONES INTERPRETAR, DEBUG Y LABEL POSICIÓN ##################################
        self.textConsola = Entry(self.root, width=10)
        self.btnInterpretar = Button(self.root, text="Interpretar", bg='red', command=self.btn_run)
        self.btnDebug = Button(self.root, text="Debugger", bg='red')
        self.lblPos = Label(self.root, text="Línea:0 Columna:0")
        self.lblPos.pack()
        self.lblPos.place(x=600, y=570)

        ############################### CREAR EDITORES Y COLOCAR POSICION #############################
        self.txt = ScrollText(self.root)
        self.txt.insert(END, '\n')
        self.txt.place(x=30, y=40)

        self.textConsola = scrolledtext.ScrolledText(
        self.root, width=70, height=32, bg="#cccccc", fg="#1a1a1a")
        self.textConsola.place(x=750, y=40)

        self.btnInterpretar.place(x=300, y=10)
        self.btnDebug.place(x=400, y=10)

        ###################### EVENTOS PARA ACTUALIZAR POSICION ##########################
        self.txt.text.bind("<ButtonRelease-1>", self.posicion)
        self.txt.text.bind("<KeyPress>", self.posicion)
        self.txt.text.bind("<Button-1>", self.posicion)
        #self.txt.text.bind('<KeyRelease>', self.pintarEscribit) #EVENTO PARA PINTAR AL ESCRIBIR (CORREGIR)

        ################## PINTAR PALABRAS AL CARGAR ARCHIVO ############################
        self.txt.tag_config('reservada', color='blue')
        self.txt.tag_config('string', color='orange red')
        self.txt.tag_config('comentarioU', color='gray38')
        self.txt.tag_config('numero', color='magenta3')
            

    def actualizarConsola(self, contConsola):
        self.textConsola.delete("1.0", END)
        self.textConsola.insert("1.0", contConsola)

    def run(self):
        self.root.mainloop()

    '''def pintarEscribit(self,*args):  #colorear palabras mientras se escriben
        entrada = self.txt.get("1.0", END)
        posicion = self.txt.text.index(INSERT)
        self.txt.delete("1.0", END)
        #print(self.recorrerEntrada(entrada))
        for s in self.recorrerEntrada(entrada[0:len(entrada)-1]):
            self.txt.insert(INSERT, s[1], s[0])
        self.txt.text.mark_set(INSERT, posicion)
        self.txt.text.see(INSERT)'''

    def posicion(self, *args, **kwargs):
        posicion = self.txt.text.index(INSERT)
        posicion2 = posicion.split(".")
        self.lblPos.destroy()
        self.lblPos = Label(
            self.root, text=f"Línea: {posicion2[0]} Columna: {int(posicion2[1])+1}")
        self.lblPos.pack()
        self.lblPos.place(x=600, y=570)

    def new_file(self):
        self.fileName = ""
        self.txt.delete(1.0, END)
        self.textConsola.delete(1.0, END)

    def open_file(self):
        self.fileName = filedialog.askopenfilename(
            title="Seleccionar archivo", initialdir="./", filetypes=(("All Files", "*.*"), (".jpr", "*.jpr")))
        if self.fileName != "":
            file = open(self.fileName, "r")
            content = file.read()
            self.txt.delete("1.0", END)
            for s in self.recorrerEntrada(content):
                self.txt.insert(INSERT, s[1], s[0])
            file.close()

    def saveAs_file(self):
        guardar = filedialog.asksaveasfilename(
            title="Guardar Archivo", initialdir="C:/", filetypes=(("Archivo jpr", "*.jpr"), ("rmt files", "*.rmt")))
        print("guaradasd ", guardar)
        fguardar = open(guardar, "w")
        fguardar.write(self.txt.get(1.0, END))
        fguardar.close()
        self.fileName = guardar

    def save_file(self):
        if self.fileName == "":
            guardar = filedialog.asksaveasfilename(
                title="Guardar Archivo", initialdir="C:/", filetypes=((".jpr", "*.jpr"), ("rmt files", "*.rmt")))
            print("guaradasd ", guardar)
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
        from TS.TablaSimbolos import listaTablaSimbolos
        listaTablaSimbolos.clear()
        listaErrores.clear()
        entrada = ""
        entrada = self.txt.get("1.0", END)
        self.textConsola.delete("1.0", END)
        salidaConsola = ejecutar(entrada, self.textConsola)
        self.textConsola.delete("1.0", END)
        self.textConsola.insert("1.0", salidaConsola)

    def recorrerEntrada(self, entrada):  #RECORRER ENTRADA PARA PINTAR
        #entrada = entrada + " "
        lista = []
        val = ''
        counter = 0
        while counter < len(entrada):
            if re.search(r"[a-zA-Z_]", entrada[counter], re.IGNORECASE):
                val += entrada[counter]
            elif entrada[counter] == "$":
                if len(val) != 0:
                    l = []
                    l.append("variable")
                    l.append(val)
                    print("primer if",l)
                    lista.append(l)
                    val = ''
                    val = "$"

            elif entrada[counter] == "\"": #inicio de capatura para las cadenas
                if len(val) != 0:
                    l = []
                    l.append("variable")
                    l.append(val)
                    lista.append(l)
                    val = ''
                val = entrada[counter]
                counter += 1
                while counter < len(entrada):
                    if entrada[counter] == "\"": #recorrer concatenar hasta encontrar fin de cadena
                        val += entrada[counter]
                        l = []
                        l.append("string")
                        l.append(val)
                        lista.append(l)
                        val = ''
                        break
                    val += entrada[counter]
                    counter += 1

            elif entrada[counter] == "#" and entrada[counter+1] != "*" and entrada[counter-1] != "*": #inicio de comentario
                if len(val) != 0:
                    l = []
                    l.append("variable")
                    l.append(val)
                    lista.append(l)
                    val = ''
                val = entrada[counter]
                counter += 1
                while counter < len(entrada): #concatenar hasta el final dem comentario
                    if entrada[counter] == "\n":
                        val += entrada[counter]
                        l = []
                        l.append("comentarioU")
                        l.append(val)
                        lista.append(l)
                        val = ''
                        break
                    val += entrada[counter]
                    counter += 1

            elif entrada[counter] == "#" and entrada[counter+1] == "*": #inicio comentario multilinea
                if len(val) != 0:
                    l = []
                    l.append("variable")
                    l.append(val)
                    lista.append(l)
                    val = ''
                val = entrada[counter]
                counter += 1
                while counter < len(entrada):
                    if entrada[counter] == "#" and entrada[counter-1] == "*": #concatenar hasta final del comentario multilinea
                        val += entrada[counter]
                        l = []
                        l.append("comentarioU")
                        l.append(val)
                        lista.append(l)
                        val = ''
                        break
                    val += entrada[counter]
                    counter += 1

            elif entrada[counter] == "\'": #inicio de caracter
                if len(val) != 0:
                    l = []
                    l.append("variable")
                    l.append(val)
                    lista.append(l)
                    val = ''
                val = entrada[counter]
                counter += 1
                while counter < len(entrada):
                    if entrada[counter] == "\'": #concatenar hasta final del caracter
                        val += entrada[counter]
                        l = []
                        l.append("string")
                        l.append(val)
                        lista.append(l)
                        val = ''
                        break
                    val += entrada[counter]
                    counter += 1
            elif re.search("[0-9]", entrada[counter]) != None and re.search("[a-zA-Z_]", entrada[counter+1]) == None \
                and re.search("[a-zA-Z_]", entrada[counter-1]) == None: #CAPTURA DE NUMEROS
                if len(val) != 0:
                    l = []
                    l.append("variable")
                    l.append(val)
                    lista.append(l)
                    val = ''
                while counter < len(entrada):
                    if not re.search("[0-9]", entrada[counter]):
                        val += entrada[counter]
                        l = []
                        l.append("numero")
                        l.append(val)
                        lista.append(l)
                        val = ''
                        break
                    if not re.search("[0-9]", entrada[counter + 1]):
                        val += entrada[counter]
                        l = []
                        l.append("numero")
                        l.append(val)
                        lista.append(l)
                        val = ''
                        break
                    val += entrada[counter]
                    counter += 1
            else:
                if len(val) != 0:
                    l = []
                    l.append("variable")
                    l.append(val)
                    lista.append(l)
                    val = ''
                l = []
                l.append("signo")
                l.append(entrada[counter])
                lista.append(l)
            counter += 1
        for s in lista:
            if s[1] == 'int' or s[1] == 'double' or s[1] == 'boolean' or s[1] == 'char' or s[1] == 'string' or\
                s[1] == 'null' or s[1] == 'print' or s[1] == 'true' or s[1] == 'false' or s[1] == 'var' or s[1] == 'if' or\
                s[1] == 'else' or [1] == 'switch' or s[1] == 'case' or s[1] == 'default' or s[1] == 'while' or s[1] == 'for' or\
                s[1] == "break" or s[1]=="main":
                s[0] = 'reservada'
            elif s[1][0] != "$":
                if s[0] == 'variable':
                    s[0] = 'etiqueta'
        return lista

    def crearReporteErrores(self):
        from Reporte.CrearReporteErrores import CrearReporteErrores
        CrearReporteErrores.crearReporteErrores(None)

    def crearReporteTS(self):
        from Reporte.CrearReporteTS import CrearReporteTS
        CrearReporteTS.crearReporteErrores(None)

    def crearAST(self):
        import os
        import webbrowser
        my_path = os.path.abspath(os.path.dirname(__file__))
        path = os.path.join(my_path, f"Reporte\\ast.pdf")
        path = path.replace("\\ui", "")
        path = path.replace("\\", "/")
        print(path)
        webbrowser.open_new_tab(path)
