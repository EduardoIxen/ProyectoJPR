'''
    GRAMATICA PLY
    EDUARDO_IXEN
'''
from tkinter.constants import NO
from TS.Excepcion import Excepcion

errores = []
reservadas = {
    'int'   : 'RINT',
    'double' : 'RDOUBLE',
    'boolean': 'RBOOLEAN',
    'char' : 'RCHAR',
    'string': 'RSTRING',
    'null' : 'RNULL',
    'print' : 'RPRINT',
    'true'  : 'RTRUE',
    'false' : 'RFALSE',
}

tokens  = [
    'PUNTOCOMA', #signos
    'PARA',
    'PARC',
    'MAS', #operadores aritmeticos
    'MENOS',
    'POR',
    'DIV',
    'POTENCIA',
    'MODULO',
    'MENORQUE', #Operadores relacionales
    'MAYORQUE',
    'IGUALIGUAL',
    'IGUAL', #Operadores logicos
    'OR',
    'AND',
    'NOT',
    'DECIMAL', #datos
    'ENTERO',
    'CADENA',
    'CARACTER',
    'ID'
] + list(reservadas.values())

# Tokens
t_PUNTOCOMA     = r';'  #signos
t_PARA          = r'\('
t_PARC          = r'\)'
t_MAS           = r'\+' #aritmeticos
t_MENOS         = r'-'
t_POR           = r'\*'
t_DIV           = r'/'
t_POTENCIA      = r'\*\*'
t_MODULO        = r'\%'
t_MENORQUE      = r'<' # Relacionales
t_MAYORQUE      = r'>'
t_IGUALIGUAL    = r'=='
t_IGUAL         = r'='
t_AND           = r'&&' #Logicos
t_OR            = r'\|\|'
t_NOT           = r'!'

def t_DECIMAL(t):
    r'\d+\.\d+'
    try:
        t.value = float(t.value)
    except ValueError:
        print("Float value too large %d", t.value)
        t.value = 0
    return t

def t_ENTERO(t):
    r'\d+'
    try:
        t.value = int(t.value)
    except ValueError:
        print("Integer value too large %d", t.value)
        t.value = 0
    return t

def t_CADENA(t):
    r'(\".*\")'
    t.value = t.value[1:-1] # remuevo las comillas
    return t

def t_CARACTER(t):
    r'(\'([^\\\"]|\\.)\')'
    t.value = t.value[1:-1]
    return t

def t_ID(t):
     r'[a-zA-Z][a-zA-Z_0-9]*'
     t.type = reservadas.get(t.value.lower(),'ID')
     return t


def t_COMENTARIO_MULTI(t):
    #r'(?s)\#\*.*?\*\#'
    #r'/\*(.|\n)*?\*/'
    #r'\#\*(.|\n)*?\*\#'
    r'\#\*(.|\n)*\*\#'
    t.lexer.lineno += 1

# Comentario simple // ...
def t_COMENTARIO_SIMPLE(t):
    r'\#.*\n'
    t.lexer.lineno += 1


# Caracteres ignorados
t_ignore = " \t"

def t_newline(t):
    r'\n+'
    t.lexer.lineno += t.value.count("\n")
    
def t_error(t):
    errores.append(Excepcion("Lexico","Error léxico." + t.value[0] , t.lexer.lineno, find_column(input, t)))
    t.lexer.skip(1)

# Compute column.
#     input is the input text string
#     token is a token instance
def find_column(inp, token):
    line_start = inp.rfind('\n', 0, token.lexpos) + 1
    return (token.lexpos - line_start) + 1

def especiales(cadena):
    cadena = cadena.replace('\\n', '\n')
    cadena = cadena.replace('\\"', '\"')
    cadena = cadena.replace('\\t', '        ')
    cadena = cadena.replace("\\'","\'")
    cadena = cadena.replace('\\\\', '\\')
    cadena = cadena.replace('\\r', '\r')
    return cadena

# Construyendo el analizador léxico
import ply.lex as lex
lexer = lex.lex()


# Asociación de operadores y precedencia
precedence = (
    ('left','OR'),
    ('left','AND'),
    ('left','MENORQUE','MAYORQUE', 'IGUALIGUAL'),
    ('left','MAS','MENOS'),
    ('left', 'POR', 'DIV', 'MODULO'),
    ('right', 'POTENCIA'),
    ('right','UMENOS'),
)


# Definición de la gramática

#Abstract
from Abstract.Instruccion import Instruccion
from Instrucciones.Imprimir import Imprimir
from Expresiones.Primitivos import Primitivos
from TS.Tipo import OperadorAritmetico, TIPO
from Expresiones.Aritmetica import Aritmetica

def p_init(t) :
    'init            : instrucciones'
    t[0] = t[1]

def p_instrucciones_instrucciones_instruccion(t) :
    'instrucciones    : instrucciones instruccion'
    if t[2] != "":
        t[1].append(t[2])
    t[0] = t[1]
    
#///////////////////////////////////////INSTRUCCIONES//////////////////////////////////////////////////

def p_instrucciones_instruccion(t) :
    'instrucciones    : instruccion'
    if t[1] == "":
        t[0] = []
    else:    
        t[0] = [t[1]]

#///////////////////////////////////////INSTRUCCION//////////////////////////////////////////////////

def p_instruccion(t) :
    '''instruccion      : imprimir_instr finins'''
    t[0] = t[1]

def p_finins(t) :
    '''finins       : PUNTOCOMA
                    |'''
    t[0] = None

def p_instruccion_error(t):
    'instruccion        : error PUNTOCOMA'
    errores.append(Excepcion("Sintáctico","Error Sintáctico." + str(t[1].value) , t.lineno(1), find_column(input, t.slice[1])))
    t[0] = ""
#///////////////////////////////////////IMPRIMIR//////////////////////////////////////////////////

def p_imprimir(t) :
    'imprimir_instr     : RPRINT PARA expresion PARC'
    t[0] = Imprimir(t[3], t.lineno(1), find_column(input, t.slice[1]))

#///////////////////////////////////////EXPRESION//////////////////////////////////////////////////

def p_expresion_binaria(t):
    '''
    expresion : expresion MAS expresion
            | expresion MENOS expresion
            | expresion POR expresion
            | expresion DIV expresion
            | expresion POTENCIA expresion
            | expresion MODULO  expresion
    '''
    if t[2] == '+':
        t[0] = Aritmetica(OperadorAritmetico.MAS, t[1],t[3], t.lineno(2), find_column(input, t.slice[2]))
    elif t[2] == '-':
        t[0] = Aritmetica(OperadorAritmetico.MENOS, t[1],t[3], t.lineno(2), find_column(input, t.slice[2]))
    elif t[2] == '*':
        t[0] = Aritmetica(OperadorAritmetico.POR, t[1], t[3], t.lineno(2), find_column(input, t.slice[2]))
    elif t[2] == "/":
        t[0] = Aritmetica(OperadorAritmetico.DIV, t[1], t[3], t.lineno(2), find_column(input, t.slice[2]))
    elif t[2] == "**":
        t[0] = Aritmetica(OperadorAritmetico.POT, t[1], t[3], t.lineno(2), find_column(input, t.slice[2]))
    elif t[2] == "%":
        t[0] = Aritmetica(OperadorAritmetico.MOD, t[1], t[3], t.lineno(2), find_column(input, t.slice[2]))
        

def p_expresion_unaria(t):
    '''
    expresion : MENOS expresion %prec UMENOS
    '''
    if t[1] == "-":
        t[0] = Aritmetica(OperadorAritmetico.UMENOS, t[2], None, t.lineno(1), find_column(input, t.slice[1]))

def p_expresion_agrupacion(t):
    '''
    expresion :   PARA expresion PARC 
    '''
    t[0] = t[2]

def p_expresion_entero(t):
    '''expresion : ENTERO'''
    t[0] = Primitivos(TIPO.ENTERO,t[1], t.lineno(1), find_column(input, t.slice[1]))

def p_primitivo_decimal(t):
    '''expresion : DECIMAL'''
    t[0] = Primitivos(TIPO.DECIMAL, t[1], t.lineno(1), find_column(input, t.slice[1]))

def p_primitivo_cadena(t):
    '''expresion : CADENA'''
    t[0] = Primitivos(TIPO.CADENA, especiales(str(t[1])), t.lineno(1), find_column(input, t.slice[1]))

def p_primitivo_char(t):
    '''expresion :  CARACTER'''
    t[0] = Primitivos(TIPO.CHARACTER, especiales(str(t[1])), t.lineno(1), find_column(input, t.slice[1]))

def p_primitivo_true(t):
    '''expresion :  RTRUE'''
    t[0] = Primitivos(TIPO.BOOLEANO, True, t.lineno(1), find_column(input, t.slice[1]))

def p_primitivo_false(t):
    '''expresion :  RFALSE'''
    t[0] = Primitivos(TIPO.BOOLEANO, False, t.lineno(1), find_column(input, t.slice[1]))

import ply.yacc as yacc
parser = yacc.yacc()

input = ''

def getErrores():
    return errores

def parse(inp) :
    global errores
    global lexer
    global parser
    errores = []
    lexer = lex.lex()
    parser = yacc.yacc()
    global input
    input = inp
    return parser.parse(inp)

#INTERFAZ

def ejecutar(entrada):
    from TS.Arbol import Arbol
    from TS.TablaSimbolos import TablaSimbolos

    instrucciones = parse(entrada) #ARBOL AST
    ast = Arbol(instrucciones)
    TSGlobal = TablaSimbolos()
    ast.setTSglobal(TSGlobal)
    for error in errores:                   #CAPTURA DE ERRORES LEXICOS Y SINTACTICOS
        ast.getExcepciones().append(error)
        ast.updateConsola(error.toString())

    for instruccion in ast.getInstrucciones():      # REALIZAR LAS ACCIONES
        value = instruccion.interpretar(ast,TSGlobal)
        if isinstance(value, Excepcion) :
            ast.getExcepciones().append(value)
            ast.updateConsola(value.toString())

    print("comienzo")
    print(ast.getConsola())
    print("Func")
    return ast.getConsola()
    