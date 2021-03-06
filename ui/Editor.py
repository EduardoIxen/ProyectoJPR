import tkinter as tk
from tkinter import INSERT, END, ttk


class ScrollText(tk.Frame):
    def __init__(self, master, *args, **kwargs):
        self.cadenaPos = "" #CREAR EDITOR, INDICANDO COLOR Y FUENTE
        tk.Frame.__init__(self, *args, **kwargs)
        self.text = tk.Text(self, bg='#CCCDCD', foreground="#000000",
                            insertbackground='black',
                            selectbackground="#3333ff", width=80, height=32)

        self.text.configure(font=("Courier New", 10,'bold'))

        self.scrollbar = tk.Scrollbar(self, orient=tk.VERTICAL, command=self.text.yview)
        self.text.configure(yscrollcommand=self.scrollbar.set)

        self.numberLines = TextLineNumbers(self, width=40, bg='#737171')
        self.numberLines.attach(self.text)

        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.numberLines.pack(side=tk.LEFT, fill=tk.Y, padx=(5, 0))
        self.text.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        ################### EVENTOS PARA ACTUALIZAR NUMERO DE LINEAS DEL EDITOR ################
        self.text.bind("<Return>", self.onPressDelay)
        self.text.bind("<Enter>", self.onPressDelay)
        self.text.bind("<BackSpace>", self.onPressDelay)
        self.text.bind("<<Change>>", self.onPressDelay)
        self.text.bind("<Configure>", self.onPressDelay)
        self.text.bind("<Motion>", self.onPressDelay)
        self.text.bind("<Button-1>", self.numberLines.redraw)
        self.scrollbar.bind("<Button-1>", self.onScrollPress)
        self.text.bind("<MouseWheel>", self.onPressDelay)


    def onScrollPress(self, *args):
        self.scrollbar.bind("<B1-Motion>", self.numberLines.redraw)

    def onScrollRelease(self, *args):
        self.scrollbar.unbind("<B1-Motion>", self.numberLines.redraw)

    def onPressDelay(self, *args):
        self.after(2, self.numberLines.redraw)

    def get(self, *args, **kwargs):
        return self.text.get(*args, **kwargs)

    def insert(self, *args, **kwargs):
        return self.text.insert(*args, **kwargs)

    def delete(self, *args, **kwargs):
        return self.text.delete(*args, **kwargs)

    def see(self, *args):
        return self.text.see("end")

    def index(self, *args, **kwargs):
        return self.text.index(*args, **kwargs)

    def redraw(self):
        self.numberLines.redraw()

    def insertRed(self, word, id):
        self.text.insert(INSERT, word, id)
        self.text.tag_config(id, foreground="red")

    def tag_add(self, id, row, columnI, columnF):
        self.text.tag_add(id, row + "." + columnI, row + "." + columnF)

    def tag_config(self, id, color):
        self.text.tag_config(id, foreground=color)
    

class TextLineNumbers(tk.Canvas):
    def __init__(self, *args, **kwargs):
        tk.Canvas.__init__(self, *args, **kwargs, highlightthickness=0)
        self.textwidget = None

    def attach(self, text_widget):
        self.textwidget = text_widget

    def redraw(self, *args):
        # REESCRIBIR NUMERO DE LINEAS
        self.delete("all")

        i = self.textwidget.index("@1,0")
        while True:
            dline = self.textwidget.dlineinfo(i)
            if dline is None: break
            y = dline[1]
            linenum = str(i).split(".")[0]
            self.create_text(2, y, anchor="nw", text=linenum, fill="white")
            i = self.textwidget.index("%s+1line" % i)


