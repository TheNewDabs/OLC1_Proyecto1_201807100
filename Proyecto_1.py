import os
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
    
    def HTML():
        TxtAreaConsola.insert(INSERT, "HTML\n")
        Etiquetas = ["html", "head", "title", "body", "h1", "h2", "h3", "h4", "h5", "h6", "p", "img", "a", "ol", "ul", "li", "table", "th", "tr", "td", "caption", "colgroup", "col", "thead", "tbody", "tfoot", "foot", "br"]
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
                    Inicio = Cont
                    ColumnaI = Columna
                    FilaI = Fila
                    if Cont+1 != len(Codigo):
                        Estado = 1
                        Cont+=1
                        Columna+=1
                    else:
                        Estado == 5
                elif IsLetra(Codigo[Cont]):
                    Inicio = Cont
                    ColumnaI = Columna
                    Cont+=1
                    Columna+=1
                    Estado = 9
                elif Codigo[Cont] == ">":
                    Tokens.append(Token(">", "Simbolo_Mayor_Que", Fila, Columna))
                    TxtAreaConsola.insert(INSERT, "Simbolo | > | en Fila: " + str(Fila) + " y columna: " + str(Columna) + "\n")
                    Cont+=1
                    Columna+=1
                    if Cont < len(Codigo) and Codigo[Cont] != ">":
                        Estado = 10
                        Inicio = Cont
                        ColumnaI = Columna
                        FilaI = Fila
                    else:
                        Estado = 0
                elif Codigo[Cont] == "/":
                    Tokens.append(Token("/", "Simbolo_Barra", Fila, Columna))
                    TxtAreaConsola.insert(INSERT, "Simbolo | / | en Fila: " + str(Fila) + " y columna: " + str(Columna) + "\n")
                    Cont+=1
                    Columna+=1
                elif Codigo[Cont] == "=":
                    Tokens.append(Token("=", "Simbolo_Igual", Fila, Columna))
                    TxtAreaConsola.insert(INSERT, "Simbolo | = | en Fila: " + str(Fila) + " y columna: " + str(Columna) + "\n")
                    Cont+=1
                    Columna+=1
                elif Codigo[Cont] == "\"":
                    Estado = 11
                    Inicio = Cont
                    ColumnaI = Columna
                    FilaI = Fila
                    Cont+=1
                    Columna+=1
                elif Codigo[Cont] == " " or Codigo[Cont] == "\t" :
                    Cont+=1
                    Columna+=1
                elif Codigo[Cont] == "\n":
                    Cont+=1
                    Columna=0
                    Fila+=1
                else:
                    Errores.append(Error(Codigo[Cont], "Simbolo_No_Perteneciente", Fila, Columna))
                    TxtAreaConsola.insert(INSERT, "Error lexico: Simbolo no perteneciente | " + Codigo[Cont] + " | en Fila: " + str(Fila) + " y columna: " + str(Columna) + "\n")
                    Cont+=1
                    Columna+=1
                    Estado = 0
            elif Estado == 1:
                if Codigo[Cont] == "!" and Cont+1 != len(Codigo):
                    Estado = 2
                    Cont+=1
                    Columna+=1
                else:
                    Estado = 5
            elif Estado == 2:
                if Codigo[Cont] == "-" and Cont+1 != len(Codigo):
                    Cont+=1
                    Columna+=1
                    Estado = 3
                else:
                    Estado = 5
            elif Estado == 3:
                if Codigo[Cont] == "-" and Cont+1 != len(Codigo):
                    Cont+=1
                    Columna+=1
                    Estado = 4
                else:
                    if Cont+1 != len(Codigo):
                        Estado = 5
                    else:
                        Errores.append(Error("<!--", "Sin_Finalizar", FilaI, ColumnaI))
                        TxtAreaConsola.insert(INSERT, "Error lexico: Comentario sin finalizar | <!-- | en Fila: " + str(FilaI) + " y columna: " + str(ColumnaI) + "\n")
            elif Estado == 4:
                if Cont+1 == len(Codigo):
                    Lexema = ""
                    for i in range(Inicio, Cont):
                        Lexema += Codigo[i]
                    Errores.append(Error(Lexema, "Sin_Finalizar", Fila, Columna))
                    TxtAreaConsola.insert(INSERT, "Error lexico: Comentario sin finalizar | " + Lexema + " | en Fila: " + str(Fila) + " y columna: " + str(Columna) + "\n")
                    Estado=0
                elif Codigo[Cont] == "-":
                    Cont+=1
                    Columna+=1
                    Estado = 6
                    if Cont == len(Codigo):
                        Lexema = ""
                        for i in range(Inicio, Cont):
                            Lexema += Codigo[i]
                        Errores.append(Error(Lexema, "Sin_Finalizar", Fila, Columna))
                        TxtAreaConsola.insert(INSERT, "Error lexico: Comentario sin finalizar | " + Lexema + " | en Fila: " + str(Fila) + " y columna: " + str(Columna) + "\n")
                        Estado=0
                else:
                    if Codigo[Cont] == "\n":
                        Columna=0
                        Fila+=1
                    else:
                        Columna+=1
                    Cont+=1                 
            elif Estado == 5:
                Cont = Inicio
                Columna = ColumnaI
                Fila = FilaI
                Tokens.append(Token("<", "Simbolo_Menor_Que", Fila, Columna))
                TxtAreaConsola.insert(INSERT, "Simbolo | < | en Fila: " + str(Fila) + " y columna: " + str(Columna) + "\n")
                Cont+=1
                Columna+=1
                Estado = 0
            elif Estado == 6:
                if Codigo[Cont] == "-" and Cont+1 != len(Codigo):
                    Cont+=1
                    Columna+=1
                    Estado = 7
                elif Cont+1 == len(Codigo):
                    Lexema = ""
                    for i in range(Inicio, Cont):
                        Lexema += Codigo[i]
                    Errores.append(Error(Lexema, "Sin_Finalizar", Fila, Columna))
                    TxtAreaConsola.insert(INSERT, "Error lexico: Comentario sin finalizar | " + Lexema + " | en Fila: " + str(Fila) + " y columna: " + str(Columna) + "\n")
                    Estado=0
                else:
                    Estado = 4
            elif Estado == 7:
                if Codigo[Cont] == "!" and Cont+1 != len(Codigo):
                    Cont+=1
                    Columna+=1
                    Estado = 8
                elif Cont+1 == len(Codigo):
                    Lexema = ""
                    for i in range(Inicio, Cont):
                        Lexema += Codigo[i]
                    Errores.append(Error(Lexema, "Sin_Finalizar", Fila, Columna))
                    TxtAreaConsola.insert(INSERT, "Error lexico: Comentario sin finalizar | " + Lexema + " | en Fila: " + str(Fila) + " y columna: " + str(Columna) + "\n")
                    Estado=0
                else:
                    Estado = 4
            elif Estado == 8:
                if Codigo[Cont] == ">" and Cont+1 != len(Codigo):
                    Cont+=1
                    Columna+=1
                    Estado = 0
                    Lexema = ""
                    for i in range(Inicio, Cont):
                        Lexema += Codigo[i]
                    Tokens.append(Token(Lexema, "Comentario", FilaI, ColumnaI))
                    TxtAreaConsola.insert(INSERT, "Comentario | " + Lexema + " | en Fila: " + str(FilaI) + " y columna: " + str(ColumnaI) + "\n")
                elif Cont+1 == len(Codigo):
                    Lexema = ""
                    for i in range(Inicio, Cont):
                        Lexema += Codigo[i]
                    Errores.append(Error(Lexema, "Sin_Finalizar", FilaI, ColumnaI))
                    TxtAreaConsola.insert(INSERT, "Error lexico: Comentario sin finalizar | " + Lexema + " | en Fila: " + str(FilaI) + " y columna: " + str(ColumnaI) + "\n")
                    Estado=0
                else:
                    Estado = 4
            elif Estado == 9:
                if not IsLetra(Codigo[Cont]) and not IsDigito(Codigo[Cont]):
                    Lexema = ""
                    for i in range(Inicio, Cont):
                        Lexema += Codigo[i]
                    Etiqueta = False
                    for i in range(len(Etiquetas)):
                        if Lexema.lower() == Etiquetas[i].lower():
                            Etiqueta = True
                            Tokens.append(Token(Lexema, "Etiqueta_"+Etiquetas[i], FilaI, ColumnaI))
                            TxtAreaConsola.insert(INSERT, "Etiqueta | " + Etiquetas[i] + " | en Fila: " + str(FilaI) + " y columna: " + str(ColumnaI) + "\n")
                    if not Etiqueta:
                        Atributo = False
                        for i in range(len(Atributos)):
                            if Lexema.lower() == Atributos[i].lower():
                                Atributo = True
                                Tokens.append(Token(Lexema, "Atributo_"+Atributos[i], FilaI, ColumnaI))
                                TxtAreaConsola.insert(INSERT, "Atributo | " + Atributos[i] + " | en Fila: " + str(FilaI) + " y columna: " + str(ColumnaI) + "\n")                        
                        if not Atributo:
                            Errores.append(Error(Lexema, "Palabra_Inexistente", FilaI, ColumnaI))
                            TxtAreaConsola.insert(INSERT, "Error lexico: Etiqueta o atributo no soportado | " + Lexema + " | en Fila: " + str(FilaI) + " y columna: " + str(ColumnaI) + "\n")
                    Estado = 0
                else:
                    Cont+=1
                    Columna+=1
            elif Estado == 10:
                if Codigo[Cont] == "<":
                    Lexema = ""
                    for i in range(Inicio, Cont):
                        Lexema += Codigo[i]
                    Tokens.append(Token(Lexema, "Texto", FilaI, ColumnaI))
                    TxtAreaConsola.insert(INSERT, "Texto | " + Lexema + " | en Fila: " + str(FilaI) + " y columna: " + str(ColumnaI) + "\n")
                    Estado = 0
                else:
                    Cont+=1
                    if Cont == len(Codigo):
                        Lexema = ""
                        for i in range(Inicio, Cont):
                            Lexema += Codigo[i]
                        Tokens.append(Token(Lexema, "Texto", FilaI, ColumnaI))
                        TxtAreaConsola.insert(INSERT, "Texto | " + Lexema + " | en Fila: " + str(FilaI) + " y columna: " + str(ColumnaI) + "\n")
                        Estado = 0
                    elif Codigo[Cont] == "\n":
                        Columna = 0
                        Fila+=1
                    else:
                        Columna+=1
            elif Estado == 11:
                if Codigo[Cont] == "\"":
                    Cont+=1
                    Columna+=1
                    Lexema = ""
                    for i in range(Inicio, Cont):
                        Lexema += Codigo[i]
                    Tokens.append(Token(Lexema, "Cadena", FilaI, ColumnaI))
                    TxtAreaConsola.insert(INSERT, "Cadena | " + Lexema + " | en Fila: " + str(FilaI) + " y columna: " + str(ColumnaI) + "\n")
                    Estado = 0
                else:
                    Cont+=1
                    if Cont == len(Codigo):
                        Lexema = ""
                        for i in range(Inicio, Cont):
                            Lexema += Codigo[i]
                        Errores.append(Error(Lexema, "Cadena_Sin_Cerrar", FilaI, ColumnaI))
                        TxtAreaConsola.insert(INSERT, "Error lexico: No se cerro la cadena | " + Lexema + " | en Fila: " + str(FilaI) + " y columna: " + str(ColumnaI) + "\n")
                        Estado = 0
                    elif Codigo[Cont] == "\n":
                        Columna = 0
                        Fila+=1
                    else:
                        Columna+=1

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
                    Estado = 0
                else:
                    Estado = 2
            elif Estado == 4:
                for i in range(len(Simbolos)):
                    if Codigo[Cont] == Simbolos[i]:
                        Tokens.append(Token(Simbolos[i], "Simbolo_" + NSimbolos[i], Fila, Columna))
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
                    if not Regla:
                        Valor = False
                        for i in range(len(Valores)):
                            if Lexema == Valores[i]:
                                Valor = True
                                Tokens.append(Token(Lexema, "Valores_" + Reglas[i], FilaI, ColumnaI))
                        if not Valor:
                            Tokens.append(Token(Lexema, "ID", FilaI, ColumnaI))
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
        "Comentario Unilinea, Multilinea, Simbolos, ID, Reservadas, Numero, Decimal"
        Entrado = [False, False, False, False, False, False, False]
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

        Num=0

        def Parea(Tipo="*"):
            nonlocal Num
            nonlocal Tokens
            if Tipo != Tokens[Num].Tipo:
                Errores.append(Error(Tokens[Num].Tipo, "Incorrecto", Tokens[Num-1].Fila, (Tokens[Num-1].Columna)+1))
                TxtAreaConsola.insert(INSERT, "Error Sintactico: Viene | " + Tokens[Num].Tipo + " |, se esperaba | " + Tipo + " | en Fila: " + str(Tokens[Num].Fila) + " y columna: " + str(Tokens[Num].Columna) + "\n")
            Num+=1

        def S2():
            nonlocal Num
            nonlocal Tokens
            if Tokens[Num].Tipo == "Simbolo_Abrir_Parentesis":
                Parea("Simbolo_Abrir_Parentesis")
                if Num<len(Tokens):
                    if Tokens[Num].Tipo != "Simbolo_Cerrar_Parentesis":
                        S0()
                        if Num<len(Tokens):
                            Parea("Simbolo_Cerrar_Parentesis")
                        else:
                            Errores.append(Error(" ", "Sin_Fin", Tokens[Num-1].Fila, (Tokens[Num-1].Columna)+1))
                            TxtAreaConsola.insert(INSERT, "Error Sintactico: El parentesis nunca es cerrado\n")
                    else:
                        Errores.append(Error("", "Vacio", Tokens[Num].Fila, Tokens[Num].Columna))
                        TxtAreaConsola.insert(INSERT, "Error Sintactico: Parentesis Vacio\n")
                        Parea("Simbolo_Cerrar_Parentesis")
                else:
                    Errores.append(Error(" ", "Sin_Fin", Tokens[Num-1].Fila, (Tokens[Num-1].Columna)+1))
                    TxtAreaConsola.insert(INSERT, "Error Sintactico: El parentesis nunca es cerrado\n")
            elif Tokens[Num].Tipo == "ID":
                Parea("ID")
            else:
                Parea("Numero")

        def S1P():
            nonlocal Num
            nonlocal Tokens
            if Tokens[Num].Tipo == "Simbolo_Multilplicador":
                Parea("Simbolo_Multilplicador")
                if Num<len(Tokens):
                    S2()
                    if Num<len(Tokens):
                        S1P()
                else: 
                    Errores.append(Error(" ", "Sin_Continuar", Tokens[Num-1].Fila, (Tokens[Num-1].Columna)+1))
                    TxtAreaConsola.insert(INSERT, "Error Sintactico: No hay valor despues del signo\n")
            elif Tokens[Num].Tipo == "Simbolo_Divisor":
                Parea("Simbolo_Divisor")
                if Num<len(Tokens):
                    S2()
                    if Num<len(Tokens):
                        S1P()
                else: 
                    Errores.append(Error(" ", "Sin_Continuar", Tokens[Num-1].Fila, (Tokens[Num-1].Columna)+1))
                    TxtAreaConsola.insert(INSERT, "Error Sintactico: No hay valor despues del signo\n")

        def S1():
            nonlocal Num
            nonlocal Tokens
            if Num<len(Tokens):
                S2()
                if Num<len(Tokens):
                    S1P()

        def S0P():
            nonlocal Num
            nonlocal Tokens
            if Tokens[Num].Tipo == "Simbolo_Mas":
                Parea("Simbolo_Mas")
                if Num<len(Tokens):
                    S1()
                    if Num<len(Tokens):
                        S0P()
                else:
                    Errores.append(Error(" ", "Sin_Continuar", Tokens[Num-1].Fila, (Tokens[Num-1].Columna)+1))
                    TxtAreaConsola.insert(INSERT, "Error Sintactico: No hay valor despues del signo\n")
            elif Tokens[Num].Tipo == "Simbolo_Menos":
                Parea("Simbolo_Menos")
                if Num<len(Tokens):
                    S1()
                    if Num<len(Tokens):
                        S0P()
                else:
                    Errores.append(Error(" ", "Sin_Continuar", Tokens[Num-1].Fila, (Tokens[Num-1].Columna)+1))
                    TxtAreaConsola.insert(INSERT, "Error Sintactico: No hay valor despues del signo\n")

        def S0():
            nonlocal Num
            nonlocal Tokens
            if Num<len(Tokens):
                S1()
                print(Num)
                if Num<len(Tokens):
                    S0P()

        TxtAreaConsola.insert(INSERT, "Sintactico\n")
        Codigo = list(TxtAreaCodigo.get("1.0",'end-1c') + " ")
        Simbolos = ["+", "-", "*", "/", "(", ")"]
        NSimbolos = ["Mas", "Menos", "Multilplicador", "Divisor", "Abrir_Parentesis", "Cerrar_Parentesis"]
        Cont = 0
        Estado = 0
        Inicio = 0
        Columna = 0
        ColumnaI = 0
        Fila = 0
        Tokens = list()
        Errores = list()
        while Cont < len(Codigo):
            Tokens = list()
            ELexicos = 0
            while Cont < len(Codigo) and Codigo[Cont] != "\n":
                if Estado == 0:
                    if Codigo[Cont] == " " or Codigo[Cont] == "\t":
                        Cont+=1
                        Columna +=1
                    elif IsDigito(Codigo[Cont]):
                        Inicio = Cont
                        ColumnaI = Columna
                        Estado = 1
                    elif IsLetra(Codigo[Cont]):
                        Inicio = Cont
                        ColumnaI = Columna
                        Estado = 3
                    else:
                        Signo = False
                        for i in range(len(Simbolos)):
                            if Codigo[Cont] == Simbolos[i]:
                                Signo = True
                                Tokens.append(Token(Simbolos[i], "Simbolo_" + NSimbolos[i], Fila, Columna))
                                Cont+=1
                                Columna+=1
                        if not Signo:
                            ELexicos += 1
                            Errores.append(Error(Codigo[Cont], "No_Pertenece_Al_Lenguaje", Fila, Columna))
                            TxtAreaConsola.insert(INSERT, "Error lexico: El caracter no pertenece al lenguaje | " + Codigo[Cont] + " | en Fila: " + str(Fila) + " y columna: " + str(Columna) + "\n")
                            Cont+=1
                            Columna+=1
                elif Estado == 1:
                    if not IsDigito(Codigo[Cont]) and Codigo[Cont] != ".":
                        Lexema = ""
                        for i in range(Inicio, Cont):
                            Lexema += Codigo[i]
                        Tokens.append(Token(Lexema, "Numero", Fila, ColumnaI))
                        Estado = 0
                    elif Codigo[Cont] == ".":
                        Cont+=1
                        Columna+=1
                        Estado = 2
                    else:
                        Cont+=1
                        Columna+=1
                elif Estado == 2:
                    if not IsDigito(Codigo[Cont]):
                        Lexema = ""
                        for i in range(Inicio, Cont):
                            Lexema += Codigo[i]
                        Tokens.append(Token(Lexema, "Numero", Fila, ColumnaI))
                        Estado = 0
                    else:
                        Cont+=1
                        Columna+=1
                elif Estado == 3:
                    if not IsLetra(Codigo[Cont]) and not IsDigito(Codigo[Cont]):
                        Lexema = ""
                        for i in range(Inicio, Cont):
                            Lexema += Codigo[i]
                        Tokens.append(Token(Lexema, "ID", Fila, ColumnaI))
                        Estado = 0
                    else:
                        Cont+=1
                        Columna+=1
            if ELexicos != 0:
                messagebox.showwarning('Errores Lexicos', 'Se han encontrado Errores Lexicos en la operación')
            Num=0
            S0()
            if Num == len(Tokens):
                print("SI")
            else:
                print("No")
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