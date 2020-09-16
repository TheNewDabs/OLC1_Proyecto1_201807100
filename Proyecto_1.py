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
    Tokens = list()
    Errores = list()
    window = Tk()
    window.title("Analizador Lexico")
    window.geometry('648x500')
    Label(window, text="Lenguaje: ").place(x=5, y=2)
    LSelect = IntVar()
    BtnHtml = Radiobutton(window,text='HTML', value=1, variable=LSelect)
    BtnHtml.place(x=70, y=2)
    BtnCss = Radiobutton(window,text='CSS', value=2, variable=LSelect)
    BtnCss.place(x=135, y=2)
    BtnJS = Radiobutton(window,text='Javascript', value=3, variable=LSelect)
    BtnJS.place(x=180, y=2)
    BtnAS = Radiobutton(window,text='Analizador Sintactico', value=4, variable=LSelect)
    BtnAS.place(x=273, y=2)
    TxtAreaCodigo = scrolledtext.ScrolledText(window,width=77,height=15)
    TxtAreaCodigo.place(x=5, y=25)
    Label(window, text="Consola:").place(x=5, y=288)
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
        Tokens = list()
        Errores = list()
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
                    Errores.append(Error(Lexema, "Error", FilaI, ColumnaI))
                    TxtAreaConsola.insert(INSERT, "Error lexico \"" + Lexema + "\" en Fila: " + str(FilaI) + " y columna: " + str(ColumnaI) + "\n")
                    Estado = 0
                else:
                    Columna+= 1
                    Cont+= 1
                    if Codigo[Cont] == "\n":
                        Fila+=1
                        Columna = 0
            else:
                    Estado=0

    def IsLetra(Caracter="*"):
        Letras = ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "ñ", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z"]
        for i in range(len(Letras)):
            if Caracter.lower() == Letras[i].lower():
                return True
        return False
    
    def IsDigito(Caracter="*"):
        Digitos = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]
        for i in range(len(Digitos)):
            if Caracter == Digitos[i]:
                return True
        return False
    
    def CSS():
        TxtAreaConsola.insert(INSERT, "CSS\n")
        Codigo = list(TxtAreaCodigo.get("1.0",'end-1c') + " ")
        Simbolos = ["*", ".", "#", ":", ",", ";", "{", "}", "%", "(", ")", "-"]
        NSimbolos = ["Asterisco", "Punto", "Numeral", "Dos_PUntos", "Coma", "Punto_Y_Coma", "Abrir_LLaves", "Cerrar_LLave", "Porcentaje", "Abrir_Parentesis", "Cerrar_Parentesis", "Menos"]
        Reglas = ["color", "background-color", "background-image", "border", "Opacity", "background", "text-align", "font-family", "font-style", "font-weight", "font-size", "font", "padding-left", "padding-right", "padding-bottom", "padding-top", "padding", "display", "line-height", "width", "height", "margin-top", "margin-right", "margin-bottom", "margin-left", "margin", "border-style", "display", "position", "bottom", "top", "right", "left", "float", "clear", "max-width", "min-width", "max-height", "min-height"]
        Valores = ["px", "em", "vh", "vw", "in", "cm", "mm", "pt", "pc", "relative", "inline-block", "rgba", "red", "pink", "orange", "yellow", "gold", "violet", "purple", "green", "darkgreen", "cyan", "lightblue", "blue", "chocolate", "brown", "maroon", "white", "silver", "gray", "black", "url"]
        Cont = 0
        Estado = 0
        Inicio = 0
        Columna = 0
        Fila = 0
        ColumnaI = 0
        FilaI = 0
        Tokens = list()
        Errores = list()
        while Cont < len(Codigo):
            if Estado == 0:
                if Codigo[Cont] == "/":
                    Inicio = Cont
                    ColumnaI = Columna
                    Estado = 1
                    Cont+=1
                    Columna+=1
                elif Codigo[Cont] == "*" or Codigo[Cont] == "." or Codigo[Cont] == "#" or Codigo[Cont] == ":" or Codigo[Cont] == "," or Codigo[Cont] == ";" or Codigo[Cont] == "{" or Codigo[Cont] == "}":
                    Estado = 4
                elif IsLetra(Codigo[Cont]):
                    Estado = 5
                    Inicio = Cont
                    ColumnaI = Columna
                    FilaI = Fila
                    Cont+=1
                    Columna+=1
                elif IsDigito(Codigo[Cont]):
                    Estado = 6
                    Inicio = Cont
                    ColumnaI = Columna
                    FilaI = Fila
                    Cont+=1
                    Columna+=1
                elif Codigo[Cont] == "\"" or Codigo[Cont] == "“":
                    Estado = 8
                    Inicio = Cont
                    ColumnaI = Columna
                    FilaI = Fila
                    Cont+=1
                    Columna+=1
                elif Codigo[Cont] == " " or Codigo[Cont] == "\t":
                    Cont+=1
                    Columna+=1
                elif Codigo[Cont] == "\n":
                    Cont+=1
                    Columna = 0
                    Fila+=1
                else:
                    Errores.append(Error(Codigo[Cont], "Simbolo_No_Perteneciente", Fila, Columna))
                    TxtAreaConsola.insert(INSERT, "Error lexico: Simbolo no perteneciente | " + Codigo[Cont] + " | en Fila: " + str(Fila) + " y columna: " + str(Columna) + "\n")
                    Cont+=1
                    Columna+=1
                    Estado = 0
            elif Estado == 1:
                if Codigo[Cont] == "*":
                    Cont+=1
                    Columna+=1
                    Estado = 2
                else:
                    Errores.append(Error("/", "Simbolo_No_Perteneciente", FilaI, ColumnaI))
                    TxtAreaConsola.insert(INSERT, "Error lexico: Simbolo no perteneciente | / | en Fila: " + str(FilaI) + " y columna: " + str(ColumnaI) + "\n")
                    Estado = 0
            elif Estado == 2:
                if Codigo[Cont] == "*":
                    Estado = 3
                    Columna+=1
                elif Codigo[Cont] == "\n":
                    Fila += 1
                    Columna = 0
                elif Cont+1 == len(Codigo):
                    Lexema = ""
                    for i in range(Inicio, Cont):
                        Lexema += Codigo[i]
                    Errores.append(Error(Lexema, "Comentario_Sin_Fin", FilaI, ColumnaI))
                    TxtAreaConsola.insert(INSERT, "Error lexico: Comentario sin finalizar | " + Lexema + " | en Fila: " + str(FilaI) + " y columna: " + str(ColumnaI) + "\n")
                    Estado = 0
                else:
                    Columna+=1
                Cont+=1
            elif Estado == 3:
                print(Codigo[Cont])
                if Codigo[Cont] == "/":
                    Cont+=1
                    Columna+=1
                    Lexema = ""
                    for i in range(Inicio, Cont):
                        Lexema += Codigo[i]
                    Tokens.append(Token(Lexema, "Comentario", Fila, Columna))
                    TxtAreaConsola.insert(INSERT, "Comentario |" + Lexema + "| en Fila: " + str(FilaI) + " y columna: " + str(ColumnaI) + "\n")
                    Estado = 0
                else:
                    Estado = 2
            elif Estado == 4:
                for i in range(len(Simbolos)):
                    if Codigo[Cont] == Simbolos[i]:
                        Tokens.append(Token(Simbolos[i], "Simbolo_" + NSimbolos[i], Fila, Columna))
                        TxtAreaConsola.insert(INSERT, NSimbolos[i] + " |" + Simbolos[i] + "| en Fila: " + str(Fila) + " y columna: " + str(Columna) + "\n")
                        Cont+=1
                        Columna+=1
                        Estado=0
            elif Estado == 5:
                if not IsLetra(Codigo[Cont]) and not IsDigito(Codigo[Cont]) and Codigo[Cont] != "-":
                    Lexema = ""
                    for i in range(Inicio, Cont):
                        Lexema += Codigo[i]
                    Regla = False
                    for i in range(len(Reglas)):
                        if Lexema == Reglas[i]:
                            Regla = True
                            Tokens.append(Token(Lexema, "Regla_" + Reglas[i], FilaI, ColumnaI))
                            TxtAreaConsola.insert(INSERT, Reglas[i] + " |" + Lexema + "| en Fila: " + str(FilaI) + " y columna: " + str(ColumnaI) + "\n")
                    if not Regla:
                        Valor = False
                        for i in range(len(Valores)):
                            if Lexema == Valores[i]:
                                Valor = True
                                Tokens.append(Token(Lexema, "Valores_" + Reglas[i], FilaI, ColumnaI))
                                TxtAreaConsola.insert(INSERT, "Reservada de valor |" + Lexema + "| en Fila: " + str(FilaI) + " y columna: " + str(ColumnaI) + "\n")
                        if not Valor:
                            Tokens.append(Token(Lexema, "ID", FilaI, ColumnaI))
                            TxtAreaConsola.insert(INSERT, "ID |" + Lexema + "| en Fila: " + str(FilaI) + " y columna: " + str(ColumnaI) + "\n")
                    Estado = 0
                else:
                    Cont+=1
                    Columna+=1
            elif Estado == 6:
                if not IsDigito(Codigo[Cont]) and Codigo[Cont] != ".":
                    Lexema = ""
                    for i in range(Inicio, Cont):
                        Lexema += Codigo[i]
                    Tokens.append(Token(Lexema, "Numero", FilaI, ColumnaI))
                    TxtAreaConsola.insert(INSERT, "Numero |" + Lexema + "| en Fila: " + str(FilaI) + " y columna: " + str(ColumnaI) + "\n")
                    Estado = 0
                elif Codigo[Cont] == ".":
                    Cont+=1
                    Columna+=1
                    Estado = 7
                else:
                    Cont+=1
                    Columna+=1
            elif Estado == 7:
                if not IsDigito(Codigo[Cont]):
                    Lexema = ""
                    for i in range(Inicio, Cont):
                        Lexema += Codigo[i]
                    Tokens.append(Token(Lexema, "Numero_Con_Decimal", FilaI, ColumnaI))
                    TxtAreaConsola.insert(INSERT, "Numero Con Decimal |" + Lexema + "| en Fila: " + str(FilaI) + " y columna: " + str(ColumnaI) + "\n")
                    Estado = 0
                else:
                    Cont+=1
                    Columna+=1
            elif Estado == 8:
                if Cont+1 != len(Codigo):
                    if Codigo[Cont] == "\""  or Codigo[Cont] == "“":
                        Cont+=1
                        Columna+=1
                        Lexema=""
                        for i in range(Inicio, Cont):
                            Lexema += Codigo[i]
                        Tokens.append(Token(Lexema, "Cadena", FilaI, ColumnaI))
                        TxtAreaConsola.insert(INSERT, "Cadena |" + Lexema + "| en Fila: " + str(FilaI) + " y columna: " + str(ColumnaI) + "\n")
                        Estado=0
                    elif Codigo[Cont] == "\n":
                        Cont+=1
                        Columna=0
                        Fila+=1
                    else:
                        Cont+=1
                        Columna+=1
                else:
                    Errores.append(Error(Lexema, "Cadena_Sin_Fin", FilaI, ColumnaI))
                    TxtAreaConsola.insert(INSERT, "Error lexico: Cadena sin finalizar | " + Lexema + " | en Fila: " + str(FilaI) + " y columna: " + str(ColumnaI) + "\n")
                    Estado = 0
                
    def Javascript():
        TxtAreaConsola.insert(INSERT, "JS\n")
        Codigo = list(TxtAreaCodigo.get("1.0",'end-1c') + " ")
        NCodigo = ""
        Simbolos = ["=", "*", ";", "(", ")", "{", "}", ".", "<", ">", "+", "-", "/", ",", "!", "&", "|", ":" ]
        NSimbolos = ["Igual", "Asterisco", "Punto_Y_Coma", "Abrir_Parentesis", "Cerrar_Parentesis", "Abrir_Llaves", "Cerrar_Llaves", "Punto", "Menor_Que", "Mayor_Que", "Mas", "Menos", "Barra", "Coma", "Negacion", "Ampersand", "Pleca", "Dos_Puntos"]
        Reservadas = ["var", "if", "else", "for", "while", "do", "continue", "break", "return", "function", "constructor", "class", "this", "Math", "pow", "console", "log"]
        Cont = 0
        Estado = 0
        Inicio = 0
        Columna = 0
        Fila = 0
        ColumnaI = 0
        FilaI = 0
        Tokens = list()
        Errores = list()
        while Cont < len(Codigo):
            if Estado == 0:
                if Codigo[Cont] == "/":
                    Inicio = Cont
                    ColumnaI = Columna
                    FilaI = Fila
                    Estado = 1
                    Cont+=1
                    Columna+=1
                elif IsLetra(Codigo[Cont]):
                    Inicio = Cont
                    ColumnaI = ColumnaI
                    FilaI = Fila
                    Cont+=1
                    Columna+=1
                    Estado = 5
                elif IsDigito(Codigo[Cont]):
                    Estado = 6
                    Inicio = Cont
                    ColumnaI = Columna
                    FilaI = Fila
                    Cont+=1
                    Columna+=1
                elif Codigo[Cont] == "\t" and Codigo[Cont] ==  "":
                    NCodigo += Codigo[Cont]
                    Cont+=1
                    Columna+=1
                elif Codigo[Cont] == "\n":
                    NCodigo += Codigo[Cont]
                    Cont+=1
                    Columna = 0
                    Fila+=1
                else:
                    Signo = False
                    for i in range(len(Simbolos)):
                        if Codigo[Cont] == Simbolos[i]:
                            Signo = True
                            Tokens.append(Token(Simbolos[i], "Simbolo_" + NSimbolos[i], Fila, Columna))
                            NCodigo += Codigo[Cont]
                            Cont+=1
                            Columna+=1
                    if not Signo:
                        Errores.append(Error(Codigo[Cont], "No_Pertenece_Al_Lenguaje", Fila, Columna))
                        TxtAreaConsola.insert(INSERT, "Error lexico: El caracter no pertenece al lenguaje | " + Codigo[Cont] + " | en Fila: " + str(Fila) + " y columna: " + str(Columna) + "\n")
                        Cont+=1
                        Columna+=1
            elif Estado == 1:
                print(Codigo[Cont])
                if Codigo[Cont] == "/":
                    Estado = 2
                    Cont+=1
                    Columna+=1
                elif Codigo[Cont] == "*":
                    Estado = 3
                    Cont+=1
                    Columna+=1
                else:
                    Tokens.append(Token(Codigo[Cont-1], "Simbolo_Barra", Fila, Columna-1))
                    NCodigo += "/"
                    Estado = 0
            elif Estado == 2:
                if Cont+1 == len(Codigo) or Codigo[Cont] == "\n":
                    Lexema = ""
                    for i in range(Inicio, Cont):
                        Lexema += Codigo[i]
                    Tokens.append(Token(Lexema, "Comentario", FilaI, ColumnaI))
                    NCodigo += Lexema
                    Estado = 0
                else:
                    Cont+=1
                    Columna+=1
            elif Estado == 3:
                if Codigo[Cont] == "*":
                    Estado = 4
                    Cont+=1
                    Columna+=1
                elif Cont+1==len(Codigo):
                    Lexema = ""
                    for i in range(Inicio, Cont):
                        Lexema += Codigo[i]
                    Errores.append(Error(Lexema, "Comentario_Sin_Fin", FilaI, ColumnaI))
                    TxtAreaConsola.insert(INSERT, "Error lexico: Comentario sin finalizar | " + Lexema + " | en Fila: " + str(FilaI) + " y columna: " + str(ColumnaI) + "\n")
                    Estado = 0
                elif Codigo[Cont] == "\n":
                    Cont+=1
                    Columna = 0
                    Fila+=1
                else:
                    Cont+=1
                    Columna+=1
            elif Estado == 4:
                if Codigo[Cont] == "/":
                    Cont+=1
                    Columna+=1
                    Lexema = ""
                    for i in range(Inicio, Cont):
                        Lexema += Codigo[i]
                    Tokens.append(Token(Lexema, "Comentario", FilaI, ColumnaI))
                    NCodigo += Lexema
                    Estado = 0
                else:
                    Estado = 3
            elif Estado == 5:
                if not IsLetra(Codigo[Cont]) and not IsDigito(Codigo[Cont]):
                    Lexema = ""
                    for i in range(Inicio, Cont):
                        Lexema += Codigo[i]
                    Reservada = False
                    for i in range(len(Reservadas)):
                        if Lexema == Reservadas[i]:
                            Reservada = True
                            Tokens.append(Token(Lexema, "Reservada_" + Reservadas[i], FilaI, ColumnaI))
                            NCodigo += Lexema
                    if not Reservada:
                        Tokens.append(Token(Lexema, "ID", FilaI, ColumnaI))
                        NCodigo += Lexema
                    Estado = 0
                else:
                    Cont+=1
                    Columna+=1
            elif Estado == 6:
                if not IsDigito(Codigo[Cont]) and Codigo[Cont] != ".":
                    Lexema = ""
                    for i in range(Inicio, Cont):
                        Lexema += Codigo[i]
                    Tokens.append(Token(Lexema, "Numero", FilaI, ColumnaI))
                    NCodigo += Lexema
                    Estado = 0
                elif Codigo[Cont] == ".":
                    Cont+=1
                    Columna+=1
                    Estado = 7
                else:
                    Cont+=1
                    Columna+=1
            elif Estado == 7:
                if not IsDigito(Codigo[Cont]):
                    Lexema = ""
                    for i in range(Inicio, Cont):
                        Lexema += Codigo[i]
                    Tokens.append(Token(Lexema, "Numero_Con_Decimal", FilaI, ColumnaI))
                    NCodigo += Lexema
                    Estado = 0
                else:
                    Cont+=1
                    Columna+=1
        TxtAreaCodigo.delete(1.0,END)
        TxtAreaCodigo.insert(INSERT, NCodigo)

    def Sintactico():
        TxtAreaConsola.insert(INSERT, "Sintactico\n")
        Codigo = list(TxtAreaCodigo.get("1.0",'end-1c') + " ")
        Simbolos = ["+", "-", "*", "/", "^"]
        NSimbolos = ["Mas", "Menos", "Multilplicador", "Divisor", "Potencia"]
        Cont = 0
        Estado = 0
        Inicio = 0
        Columna = 0
        Fila = 0
        Tokens = list()
        Errores = list()
        while Cont < len(Codigo):
            ELexicos = 0
            while Codigo[Cont] != "\n":
                if Estado == 0:
                    if Codigo[Cont] == " " or Codigo[Cont] == "\t":
                        Cont+=1
                        Columna +=1
                    elif IsDigito(Codigo[Cont]):
                        Estado = 1
                    elif IsLetra(Codigo[Cont]):
                        Estado = 2
                    else:
                        Signo = False
                        for i in range(len(Simbolos)):
                            if Codigo[Cont] == Simbolos[i]:
                                Signo = True
                                Tokens.append(Token(Simbolos[i], "Simbolo_" + NSimbolos[i], Fila, Columna))
                                NCodigo += Codigo[Cont]
                                Cont+=1
                                Columna+=1
                        if not Signo:
                            Errores.append(Error(Codigo[Cont], "No_Pertenece_Al_Lenguaje", Fila, Columna))
                            TxtAreaConsola.insert(INSERT, "Error lexico: El caracter no pertenece al lenguaje | " + Codigo[Cont] + " | en Fila: " + str(Fila) + " y columna: " + str(Columna) + "\n")
                            Cont+=1
                            Columna+=1
            Columna=0
            Fila += 1 
            Cont+=1
    
    def Analizar():
        Tokens = list()
        TxtAreaConsola.configure(state="normal")
        switcher = {
            1: HTML,
            2: CSS,
            3: Javascript,
            4: Sintactico
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