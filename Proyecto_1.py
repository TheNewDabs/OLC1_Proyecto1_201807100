from tkinter import *
from tkinter import Menu
from tkinter import scrolledtext
from tkinter import messagebox

class Token(object):
    def __init__(self, Lexema="*", Tipo="*", Fila=0, Columna=0):
        self.Lexema = Lexema
        self.Tipo = Tipo
        self.Fila = Fila
        self.Columna = Columna
        
class Error(object):
    def __init__(self, Lexema="*", Tipo="*", Fila=0, Columna=0):
        self.Lexema = Lexema
        self.Tipo = Tipo
        self.Fila = Fila
        self.Columna = Columna
#Main
        
try:
    Tokens = list();
    Errores = list();
    window = Tk()
    window.title("Analizador Lexico")
    window.geometry('648x500')
    Lbl1 = Label(window, text="Lenguaje: ").place(x=5, y=2)
    LSelect = IntVar()
    BtnHtml = Radiobutton(window,text='HTML', value=1, variable=LSelect)
    BtnHtml.place(x=70, y=2)
    BtnCss = Radiobutton(window,text='CSS', value=2, variable=LSelect)
    BtnCss.place(x=135, y=2)
    BtnJS = Radiobutton(window,text='Javascript', value=3, variable=LSelect)
    BtnJS.place(x=180, y=2)
    TxtAreaCodigo = scrolledtext.ScrolledText(window,width=77,height=15)
    TxtAreaCodigo.place(x=5, y=25)
    Lbl2 = Label(window, text="Consola:").place(x=5, y=288)
    TxtAreaConsola = scrolledtext.ScrolledText(window,width=77,height=10, state='disabled')
    TxtAreaConsola.place(x=5, y=310)
    menu = Menu(window)
    new_item = Menu(menu, tearoff=0)
    new_item.add_command(label='Nuevo Archivo')
    new_item.add_command(label='Abrir Archivo')
    new_item.add_separator()
    new_item.add_command(label='Guardar')
    new_item.add_command(label='Guardar como')
    menu.add_cascade(label='Archivo', menu=new_item)
    
    def HTML():
        TxtAreaConsola.insert(INSERT, "HTML\n")
        Etiquetas = ["html", "head", "title", "body", "h1", "h2", "h3", "h4", "h5", "h6", "p", "img", "a", "ol", "ul", "li", "table", "th", "tr", "td", "caption", "colgroup", "col", "thead", "tbody", "tfoot", "foot", "br"]
        Texto = ["title", "h1", "h2", "h3", "h4", "h5", "h6", "p", "a", "li", "th", "td", "caption", "br"]
        Atributos = ["src", "href", "style", "border"]
        Codigo = list(TxtAreaCodigo.get("1.0",'end-1c') + " ")
        Cont = 0
        Estado = 0
        Inicio = 0
        Columna = 0
        Fila = 0
        ColumnaI = 0
        FilaI = 0
        Cerradura = False
        Tokens = list();
        Errores = list();
        while Cont < len(Codigo):
            if Estado == 0:
                if Codigo[Cont] == "<":
                    Tokens.append(Token("<", "Simbolo_Menor_Que", Fila, Columna))
                    TxtAreaConsola.insert(INSERT, "Simbolo Menor Que \"<\" en Fila: " + str(Fila) + " y columna: " + str(Columna) + "\n")
                    Columna+=1
                    Cont+=1
                    if Codigo[Cont] == "/":
                        Tokens.append(Token("/", "Simbolo_Barra", Fila, Columna))
                        TxtAreaConsola.insert(INSERT, "Simbolo Barra \"/\" en Fila: " + str(Fila) + " y columna: " + str(Columna) + "\n")
                        Cont+= 1
                        Columna+=1
                        Cerradura = True
                    else:
                        Cerradura = False
                    Estado = 1
                    ColumnaI = Columna
                    FilaI = FilaI
                    Inicio = Cont
                    if Codigo[Cont] == "!" and Cont+1 != len(Codigo):
                        Cont+=1
                        Columna+=1
                        if Codigo[Cont] == "-" and Cont+1 != len(Codigo):
                            Cont+=1
                            Columna+=1
                            if Codigo[Cont] == "-" and Cont+1 != len(Codigo):
                                Tokens.append(Token("!", "Simbolo_Exclamacion", FilaI, ColumnaI))
                                TxtAreaConsola.insert(INSERT, "Simbolo Exclamacion \"!\" en Fila: " + str(FilaI) + " y columna: " + str(ColumnaI) + "\n")
                                Tokens.append(Token("-", "Simbolo_Guion", FilaI, ColumnaI+1))
                                TxtAreaConsola.insert(INSERT, "Simbolo Guion \"-\" en Fila: " + str(FilaI) + " y columna: " + str(ColumnaI+1) + "\n")
                                Tokens.append(Token("-", "Simbolo_Exclamacion", FilaI, Columna))
                                TxtAreaConsola.insert(INSERT, "Simbolo Guion \"-\" en Fila: " + str(FilaI) + " y columna: " + str(Columna) + "\n")
                                Cont+=1
                                Columna+=1
                                ColumnaI = Columna
                                FilaI = FilaI
                                Inicio = Cont
                                Estado = 5
                            else:
                                Cont = Inicio
                                Columna = ColumnaI
                        else:
                            Cont = Inicio
                            Columna = ColumnaI
                elif Codigo[Cont] == ">":
                    Tokens.append(Token(">", "Simbolo_Mayor_Que", Fila, Columna))
                    TxtAreaConsola.insert(INSERT, "Simbolo Mayor Que \">\" en Fila: " + str(Fila) + " y columna: " + str(Columna) + "\n")
                    Columna+=1
                    Cont+=1
                elif Codigo[Cont] == " " or Codigo[Cont] == "\t" or Codigo[Cont] == "":
                    Cont+= 1
                    Columna+= 1
                elif Codigo[Cont] == "\n":
                    Cont+= 1
                    Columna = 0
                    Fila+= 1
                else:
                    ColumnaI = Columna
                    FilaI = Fila
                    Inicio = Cont
                    Estado = 100
            elif Estado == 1:
                if Codigo[Cont] == " " or Codigo[Cont] == "\t" or  Codigo[Cont] == "\n" or  Codigo[Cont] == ">" or  Codigo[Cont] == "/":
                    Lexema = ""
                    for i in range(Inicio, Cont):
                        Lexema += Codigo[i]
                    print(Lexema)
                    Etiqueta = False
                    for i in range(len(Etiquetas)):
                        if Lexema.lower() == Etiquetas[i].lower():
                            Tokens.append(Token(Lexema, "Etiqueta_" + Etiquetas[i], FilaI, ColumnaI))
                            TxtAreaConsola.insert(INSERT, "Etiqueta " + Etiquetas[i] + " en Fila: " + str(FilaI) + " y columna: " + str(ColumnaI) + "\n")
                            Etiqueta = True
                    if Etiqueta:
                        if Codigo[Cont] == "\n":
                            Estado == 0
                        elif Codigo[Cont] == " " or Codigo[Cont] == "\t" or Codigo[Cont] == ">" or Codigo[Cont] == "/":
                            if Codigo[Cont] == "/":
                                Tokens.append(Token("/", "Simbolo_Barra", Fila, Columna))
                                TxtAreaConsola.insert(INSERT, "Simbolo Barra \"/\" en Fila: " + str(Fila) + " y columna: " + str(Columna) + "\n")
                                Columna+=1
                                Cont+=1
                            while (Codigo[Cont] == " " or Codigo[Cont] == "\t") and Cont+1 != len(Codigo):
                                Columna+=1
                                Cont+=1
                            if Cont != len(Codigo):
                                Text = False
                                for i in range(len(Texto)):
                                    if Lexema.lower() == Texto[i].lower():
                                        Text = True
                                if Codigo[Cont] == ">":
                                    Tokens.append(Token(">", "Simbolo_Mayor_Que", Fila, Columna))
                                    TxtAreaConsola.insert(INSERT, "Simbolo Mayor Que \">\" en Fila: " + str(Fila) + " y columna: " + str(Columna) + "\n")
                                    Columna+=1
                                    Cont+=1
                                    if Text and not Cerradura:
                                        Estado = 3
                                        Inicio = Cont
                                        FilaI = Fila
                                        ColumnaI = Columna
                                    else:
                                        Estado = 0
                                else:
                                    Inicio = Cont
                                    FilaI = Fila
                                    ColumnaI = Columna
                                    Estado = 2
                    else:
                        Errores.append(Error(Lexema, "Error", FilaI, ColumnaI))
                        TxtAreaConsola.insert(INSERT, "Error lexico \"" + Lexema + "\" en Fila: " + str(FilaI) + " y columna: " + str(ColumnaI) + "\n")
                        Estado = 0
                else:
                    Cont+=1
                    Columna+=1
            elif Estado == 2:
                if Codigo[Cont] == " " or Codigo[Cont] == "\t" or  Codigo[Cont] == "\n" or  Codigo[Cont] == ">" or  Codigo[Cont] == "/" or  Codigo[Cont] == "=":
                    Lexema = ""
                    for i in range(Inicio, Cont):
                        Lexema += Codigo[i]
                    Atributo = False
                    for i in range(len(Atributos)):
                        if Lexema.lower() == Atributos[i].lower():
                            Tokens.append(Token(Lexema, "Atributo_" + Atributos[i], FilaI, ColumnaI))
                            TxtAreaConsola.insert(INSERT, "Atributos " + Atributos[i] + " en Fila: " + str(FilaI) + " y columna: " + str(ColumnaI) + "\n")
                            Atributo = True
                    if Atributo:
                        if Codigo[Cont] == "\n":
                            Estado == 0
                        elif Codigo[Cont] == " " or Codigo[Cont] == "\t" or Codigo[Cont] == ">" or Codigo[Cont] == "=":
                            while (Codigo[Cont] == " " or Codigo[Cont] == "\t") and Cont+1 != len(Codigo):
                                Columna+=1
                                Cont+=1
                            if Cont != len(Codigo):
                                if Codigo[Cont] == ">":
                                    Tokens.append(Token(">", "Simbolo_Mayor_Que", Fila, Columna))
                                    TxtAreaConsola.insert(INSERT, "Simbolo Mayor Que \">\" en Fila: " + str(Fila) + " y columna: " + str(Columna) + "\n")
                                    Columna+=1
                                    Cont+=1
                                    if Text:
                                        ColumnaI = Columna
                                        FilaI = Fila
                                        Estado = 3
                                    else:
                                        Estado = 0
                                elif Codigo[Cont] == "=":
                                    Tokens.append(Token("=", "Simbolo_Igual_Que", Fila, Columna))
                                    TxtAreaConsola.insert(INSERT, "Simbolo Igual Que \"=\" en Fila: " + str(Fila) + " y columna: " + str(Columna) + "\n")
                                    Columna+=1
                                    Cont+=1
                                    if Codigo[Cont] == "\"":
                                        Tokens.append(Token("\"", "Simbolo_Comillas", Fila, Columna))
                                        TxtAreaConsola.insert(INSERT, "Simbolo Comillas [\"] en Fila: " + str(Fila) + " y columna: " + str(Columna) + "\n")
                                        Columna+=1
                                        Cont+=1
                                        Estado = 4
                                        Inicio = Cont
                                        FilaI = Fila
                                        ColumnaI = Columna
                                    else:
                                        Estado = 0
                                else:
                                    Inicio = Cont
                                    FilaI = Fila
                                    ColumnaI = Columna
                    else:
                        Errores.append(Error(Lexema, "Error", FilaI, ColumnaI))
                        TxtAreaConsola.insert(INSERT, "Error lexico \"" + Lexema + "\" en Fila: " + str(FilaI) + " y columna: " + str(ColumnaI) + "\n")
                        Estado = 0
                else:
                    Cont+=1
                    Columna+=1
            elif Estado == 3:
                while Cont+1 != len(Codigo) and Codigo[Cont] != "<":
                    Cont+=1
                    Columna+=1
                    if Codigo[Cont] == "\n":
                        Fila+=1
                        Columna = 0
                Lexema = ""
                for i in range(Inicio, Cont):
                    Lexema += Codigo[i]
                Tokens.append(Token(Lexema, "Cadena", Fila, Columna))
                TxtAreaConsola.insert(INSERT, "Cadena \"" + Lexema + "\" en Fila: " + str(Fila) + " y columna: " + str(Columna) + "\n")
                Estado = 0
            elif Estado == 4:
                while Cont+1 != len(Codigo) and Codigo[Cont] != "\"":
                    Cont+=1
                    Columna+=1
                    if Codigo[Cont] == "\n":
                        Fila+=1
                        Columna = 0
                Lexema = ""
                for i in range(Inicio, Cont):
                    Lexema += Codigo[i]
                if Codigo[Cont] == "\"":
                    Tokens.append(Token(Lexema, "Texto", Fila, Columna))
                    TxtAreaConsola.insert(INSERT, "Texto \"" + Lexema + "\" en Fila: " + str(Fila) + " y columna: " + str(Columna) + "\n")
                    Tokens.append(Token("\"", "Simbolo_Comillas", Fila, Columna))
                    TxtAreaConsola.insert(INSERT, "Simbolo Comillas [\"] en Fila: " + str(Fila) + " y columna: " + str(Columna) + "\n")
                    Cont+=1
                    Columna+=1
                    while (Codigo[Cont] == " " or Codigo[Cont] == "\t") and Cont+1 != len(Codigo):
                        Columna+=1
                        Cont+=1
                    if Codigo[Cont] == ">":
                        Tokens.append(Token(">", "Simbolo_Mayor_Que", Fila, Columna))
                        TxtAreaConsola.insert(INSERT, "Simbolo Mayor Que \">\" en Fila: " + str(Fila) + " y columna: " + str(Columna) + "\n")
                        Columna+=1
                        Cont+=1
                        if Text:
                            Inicio = Cont
                            ColumnaI = Columna
                            FilaI = Fila
                            Estado = 3
                        else:
                            Estado = 0
                    else:
                        Estado = 2
                        Inicio = Cont
                        ColumnaI = Columna
                        FilaI = Fila
                else:
                    Errores.append(Error(Lexema, "Error", FilaI, ColumnaI))
                    TxtAreaConsola.insert(INSERT, "Error lexico \"" + Lexema + "\" en Fila: " + str(FilaI) + " y columna: " + str(ColumnaI) + "\n")
                    Estado = 0
            elif Estado == 5:
                while Cont+1 != len(Codigo) and Codigo[Cont] != "-":
                    Cont+=1
                    Columna+=1
                    if Codigo[Cont] == "\n":
                        Fila+=1
                        Columna = 0
                if Cont+1 != len(Codigo) and Codigo[Cont] == "-":
                    Cont+=1
                    Columna+=1
                    if Cont+1 != len(Codigo) and Codigo[Cont] == "-":
                        Cont+=1
                        Columna+=1
                        if Cont+1 != len(Codigo) and Codigo[Cont] == "!":
                            Cont+=1
                            Columna+=1
                            if Cont+1 != len(Codigo) and Codigo[Cont] == ">":
                                Lexema = ""
                                for i in range(Inicio, Cont-3):
                                    Lexema += Codigo[i]
                                Tokens.append(Token(Lexema, "Comentario", Fila, Columna))
                                TxtAreaConsola.insert(INSERT, "Comentario \"" + Lexema + "\" en Fila: " + str(Fila) + " y columna: " + str(Columna) + "\n")
                                Tokens.append(Token("-", "Simbolo_Exclamacion", Fila, Columna-3))
                                TxtAreaConsola.insert(INSERT, "Simbolo Guion \"-\" en Fila: " + str(Fila) + " y columna: " + str(Columna-3) + "\n")
                                Tokens.append(Token("-", "Simbolo_Exclamacion", Fila, Columna-2))
                                TxtAreaConsola.insert(INSERT, "Simbolo Guion \"-\" en Fila: " + str(Fila) + " y columna: " + str(Columna-2) + "\n")
                                Tokens.append(Token("!", "Simbolo_Exclamacion", Fila, Columna-1))
                                TxtAreaConsola.insert(INSERT, "Simbolo Exclamacion \"!\" en Fila: " + str(Fila) + " y columna: " + str(Columna-1) + "\n")
                                Tokens.append(Token(">", "Simbolo_Mayor_Que", Fila, Columna))
                                TxtAreaConsola.insert(INSERT, "Simbolo Mayor Que \">\" en Fila: " + str(Fila) + " y columna: " + str(Columna) + "\n")
                                Cont+=1
                                Columna+=1
                                Estado = 0
                elif Cont+1 == len(Codigo):
                    Lexema = ""
                    for i in range(Inicio, Cont+1):
                        Lexema += Codigo[i]
                    Errores.append(Error(Lexema, "Error", Fila, Columna))
                    TxtAreaConsola.insert(INSERT, "Error lexico \"" + Lexema + "\" en Fila: " + str(FilaI) + " y columna: " + str(ColumnaI) + "\n")
                    Estado = 0
            elif Estado == 100:
                if Codigo[Cont] == "<" or Codigo[Cont]== "\n" or Cont+1 == len(Codigo):
                    Lexema = ""
                    if Cont+1 == len(Codigo):
                        Cont+=1
                    for i in range(Inicio, Cont):
                        Lexema += Codigo[i]
                    Errores.append(Error(Lexema, "Error", Fila, Columna))
                    TxtAreaConsola.insert(INSERT, "Error lexico \"" + Lexema + "\" en Fila: " + str(FilaI) + " y columna: " + str(ColumnaI) + "\n")
                    Estado = 0
                else:
                    Columna+= 1
                    Cont+= 1
                    if Codigo[Cont] == "\n":
                        Fila+=1
                        Columna = 0
            else:
                    T = ""
    
    def CSS():
        TxtAreaConsola.insert(INSERT, "CSS\n")
        Codigo = list(TxtAreaCodigo.get("1.0",'end-1c') + " ")
        Cont = 0
        Estado = 0
        Inicio = 0
        Columna = 0
        Fila = 0
        ColumnaI = 0
        FilaI = 0
        Tokens = list();
        Errores = list();
        while Cont < len(Codigo):
            if Estado == 0:
                if Codigo[Cont] == "/":
                    if Cont+1 != len(Codigo) and Codigo[Cont+1] == "*":
                        Cont+=2
                        Tokens.append(Token("/", "Simbolo_Barra", Fila, Columna))
                        TxtAreaConsola.insert(INSERT, "Simbolo Barra \"/\" en Fila: " + str(Fila) + " y columna: " + str(Columna) + "\n")
                        Tokens.append(Token("*", "Simbolo_Asterisco", Fila, Columna+1))
                        TxtAreaConsola.insert(INSERT, "Simbolo Asterisco \"*\" en Fila: " + str(Fila) + " y columna: " + str(Columna+1) + "\n")
                        Columna+=2
                        Estado = 1
                        Inicio = Cont
                        ColumnaI = Columna
                        FilaI = FilaI
                    else:
                        Errores.append(Error("/", "Error", Fila, Columna))
                        TxtAreaConsola.insert(INSERT, "Error lexico \"/\" en Fila: " + str(FilaI) + " y columna: " + str(ColumnaI) + "\n")
                        Cont+=1
                        Columna+=1
                elif Codigo[Cont] == " " or Codigo[Cont] == "\t" or Codigo[Cont] == "":
                    Cont+= 1
                    Columna+= 1
                elif Codigo[Cont] == "\n":
                    Cont+= 1
                    Columna = 0
                    Fila+= 1
                else:
                    Errores.append(Error(Codigo[Cont], "Error", Fila, Columna))
                    TxtAreaConsola.insert(INSERT, "Error lexico \"" + Codigo[Cont] + "\" en Fila: " + str(Fila) + " y columna: " + str(Columna) + "\n")
                    Cont+=1
                    Columna+=1
            elif Estado == 1:
                if Codigo[Cont] == "*":
                    if Cont+1 != len(Codigo) and Codigo[Cont+1] == "/":
                        Lexema = ""
                        for i in range(Inicio, Cont):
                            Lexema += Codigo[i]
                        Tokens.append(Token(Lexema, "Comentario", Fila, Columna))
                        TxtAreaConsola.insert(INSERT, "Comentario \"" + Lexema + "\" en Fila: " + str(Fila) + " y columna: " + str(Columna) + "\n")
                        Tokens.append(Token("*", "Simbolo_Asterisco", Fila, Columna))
                        TxtAreaConsola.insert(INSERT, "Simbolo Asterisco \"*\" en Fila: " + str(Fila) + " y columna: " + str(Columna+1) + "\n")
                        Tokens.append(Token("/", "Simbolo_Barra", Fila, Columna+1))
                        TxtAreaConsola.insert(INSERT, "Simbolo Barra \"/\" en Fila: " + str(Fila) + " y columna: " + str(Columna) + "\n")
                        Cont+=2
                        Columna+=2
                        Estado = 0
                    elif Cont+1 != len(Codigo):
                        Cont+=1
                        Columna+=1
                    else:
                        Lexema = ""
                        for i in range(Inicio, Cont):
                            Lexema += Codigo[i]
                        Errores.append(Error(Lexema, "Error", Fila, Columna))
                        TxtAreaConsola.insert(INSERT, "Error lexico \"" + Lexema + "\" en Fila: " + str(FilaI) + " y columna: " + str(ColumnaI) + "\n")
                        Cont+=1
                        Estado=0
                elif Cont+1 != len(Codigo):                        
                    Cont+=1
                    Columna +=1
                    if Codigo[Cont] == "\n":
                        Fila+=1
                        Columna = 0
                else:
                    Lexema = ""
                    for i in range(Inicio, Cont):
                        Lexema += Codigo[i]
                    Errores.append(Error(Lexema, "Error", Fila, Columna))
                    TxtAreaConsola.insert(INSERT, "Error lexico \"" + Lexema + "\" en Fila: " + str(FilaI) + " y columna: " + str(ColumnaI) + "\n")
                    Cont+=1
                    Columna+=1
                    Estado=0
                
    def Javascript():
        TxtAreaConsola.insert(INSERT, "JS\n")
    
    def Analizar():
        Tokens = list();
        TxtAreaConsola.configure(state="normal")
        switcher = {
            1: HTML,
            2: CSS,
            3: Javascript
        }
        func = switcher.get(LSelect.get(), lambda: messagebox.showwarning('Sin lenguaje', 'No se ah seleccionado ningun lenguaje a analizar'))
        func()
        TxtAreaConsola.configure(state="disabled")
    
    menu.add_command(label='Analizar', command=Analizar)
    menu.add_command(label='Salir')
    window.config(menu=menu)
    window.mainloop()    
except:
    messagebox.showerror('Error Inesperado', 'Porfavor reinicie el programa, de seguir susediendo comunicarse con el proveedor(io :v)')

"""Tokens.append(Token("/", "Simbolo_Barra_Inclinada", Fila, Columna))
                                    TxtAreaConsola.insert(INSERT, "Simbolo Barra Inclinada \"/\" en Fila: " + str(Fila) + " y columna: " + str(Columna) + "\n")
                        Errores.append(Error(Lexema, "Error", Fila, Columna))
                        TxtAreaConsola.insert(INSERT, "Error lexico \"" + Lexema + "\" en Fila: " + str(FilaI) + " y columna: " + str(ColumnaI) + "\n")"""
