'''
    GRAMATICA PLY
    EDUARDO_IXEN
'''
from Instrucciones.Declaracion import Declaracion
from tkinter.constants import NO
from TS.Excepcion import Excepcion
import re

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
    'var'   : 'RVAR',
    'null'  : 'RNULL',
    'if'    : 'RIF',
    'else'  : 'RELSE',
    'switch': 'RSWITCH',
    'case'  : 'RCASE',
    'default': 'RDEFAULT',
    'while' : 'RWHILE',
    'for'   : 'RFOR',
    'break' : 'RBREAK',
    'main'  : 'RMAIN'
}
#print(reservadas.keys()) -> dict_keys(['int', 'double', 'boolean', 'char'
#print(reservadas.values()) -> dict_values(['RINT', 'RDOUBLE', 'RBOOLEAN', 'RCHAR',
tokens  = [
    'PUNTOCOMA', #signos
    'PARA',
    'PARC',
    'LLAVEA',
    'LLAVEC',
    'DOSPTS',
    'MAS', #operadores aritmeticos
    'MENOS',
    'POR',
    'DIV',
    'POTENCIA',
    'MODULO',
    'MASMAS',
    'MENOSMENOS',
    'MENORQUE', #Operadores relacionales
    'MAYORQUE',
    'MENORIGUAL',
    'MAYORIGUAL',
    'IGUALIGUAL',
    'DIFERENTE',
    'IGUAL', 
    'OR', #Operadores logicos
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
t_LLAVEA        = r'{'
t_LLAVEC        = r'}'
t_DOSPTS        = r'\:'
t_MAS           = r'\+' #aritmeticos
t_MENOS         = r'-'
t_POR           = r'\*'
t_DIV           = r'/'
t_POTENCIA      = r'\*\*'
t_MODULO        = r'\%'
t_MASMAS        = r'\+\+'
t_MENOSMENOS    = r'\-\-'
t_MENORQUE      = r'<' # Relacionales
t_MAYORQUE      = r'>'
t_MENORIGUAL    = r'<='
t_MAYORIGUAL    = r'>='
t_DIFERENTE     = r'\=\!'
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
    #r'(\".*?\")'
    r'\"([^\\\"]|\\.)*\"'
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
    t.lexer.lineno += t.value.count("\n")

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
    errores.append(Excepcion("Lexico","Error lexico." + t.value[0] , t.lexer.lineno, find_column(input, t)))
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
    cadena = cadena.replace('\\t', '      ')
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
    ('right', 'UNOT'),
    ('left','MENORQUE','MAYORQUE', 'MENORIGUAL', 'MAYORIGUAL', 'IGUALIGUAL', 'DIFERENTE'),
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
from TS.Tipo import OperadorAritmetico, OperadorLogico, OperadorRelacional, TIPO
from Expresiones.Aritmetica import Aritmetica
from Expresiones.Relacional import Relacional
from Expresiones.Logica import Logica
from Instrucciones.Declaracion import Declaracion
from Expresiones.Identificador import Identificador
from Instrucciones.Asignacion import Asignacion
from Instrucciones.If import If
from Instrucciones.While import While
from Instrucciones.Break import Break
from Instrucciones.Main import Main
from Expresiones.Casteo import Casteo
from Expresiones.Incremento import Incremento
from Expresiones.Decremento import Decremento
from Instrucciones.For import For
from Instrucciones.Switch import Switch
from Instrucciones.Case import Case

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
    '''instruccion      : imprimir_instr finins
                        | declaracion_instr finins
                        | asignacion_instr finins
                        | if_instr
                        | while_instr
                        | break_instr finins
                        | main_instr
                        | incremento_instr finins
                        | decremento_instr finins
                        | for_instr
                        | switch_instr
    '''
    t[0] = t[1]

def p_finins(t) :
    '''finins       : PUNTOCOMA
                    |'''
    t[0] = None

def p_instruccion_error(t):
    'instruccion        : error PUNTOCOMA'
    errores.append(Excepcion("Sintactico","Error Sintactico." + str(t[1].value) , t.lineno(1), find_column(input, t.slice[1])))
    t[0] = ""

#///////////////////////////////////////IMPRIMIR//////////////////////////////////////////////////

def p_imprimir(t) :
    'imprimir_instr     : RPRINT PARA expresion PARC'
    t[0] = Imprimir(t[3], t.lineno(1), find_column(input, t.slice[1]))

#///////////////////////////////////////DECLARACION//////////////////////////////////////////////////
def p_declaracion(t):
    '''declaracion_instr : RVAR ID IGUAL expresion
                        | RVAR ID
    '''

    if len(t) == 5:
        t[0] = Declaracion(t[2], t.lineno(1), find_column(input, t.slice[1]), t[4])
    else:
        t[0] = Declaracion(t[2], t.lineno(1), find_column(input, t.slice[1]), None)

#///////////////////////////////////////ASIGNACION//////////////////////////////////////////////////
def p_asignacion(t):
    '''asignacion_instr : ID IGUAL expresion
    '''
    t[0] = Asignacion(t[1], t[3], t.lineno(1), find_column(input, t.slice[1]))

#///////////////////////////////////////////IF//////////////////////////////////////////////////////

def p_if1(t) :
    'if_instr     : RIF PARA expresion PARC LLAVEA instrucciones LLAVEC'
    t[0] = If(t[3], t[6], None, None, t.lineno(1), find_column(input, t.slice[1]))

def p_if2(t) :
    'if_instr     : RIF PARA expresion PARC LLAVEA instrucciones LLAVEC RELSE LLAVEA instrucciones LLAVEC'
    t[0] = If(t[3], t[6], t[10], None, t.lineno(1), find_column(input, t.slice[1]))

def p_if3(t) :
    'if_instr     : RIF PARA expresion PARC LLAVEA instrucciones LLAVEC RELSE if_instr'
    t[0] = If(t[3], t[6], None, t[9], t.lineno(1), find_column(input, t.slice[1]))

#/////////////////////////////////////// SWITCH //////////////////////////////////////////////////

def p_switch1(t):
    'switch_instr   : RSWITCH PARA expresion PARC LLAVEA case_list default LLAVEC'
    t[0] = Switch(t[3], t[6], t[7], t.lineno(1), find_column(input, t.slice[1]))

def p_switch2(t):
    'switch_instr   : RSWITCH PARA expresion PARC LLAVEA case_list LLAVEC'
    t[0] = Switch(t[3], t[6], None, t.lineno(1), find_column(input, t.slice[1]))

def p_switch3(t):
    'switch_instr   : RSWITCH PARA expresion PARC LLAVEA default LLAVEC'
    t[0] = Switch(t[3], None, t[6], t.lineno(1), find_column(input, t.slice[1]))

#/////////////////////////////////////// CASE //////////////////////////////////////////////////

def p_caseList(t):
    'case_list : case_list case'
    if t[2] != "":
        t[1].append(t[2])
    t[0] = t[1]
    

def p_caseList_simple(t):
    'case_list : case'
    if t[1] == "":
        t[0] = []
    else:    
        t[0] = [t[1]]


def p_case(t):
    'case : RCASE expresion DOSPTS instrucciones'
    t[0] = Case(t[2], t[4], t.lineno(1), find_column(input, t.slice[1]))

#/////////////////////////////////////// DEFAULT //////////////////////////////////////////////////
def p_default(t):
    'default : RDEFAULT DOSPTS instrucciones'
    t[0] = Case(None,t[3], t.lineno(1), find_column(input, t.slice[1]))


#///////////////////////////////////////WHILE//////////////////////////////////////////////////

def p_while(t):
    '''while_instr : RWHILE PARA expresion PARC LLAVEA instrucciones LLAVEC
    '''
    t[0] = While(t[3], t[6], t.lineno(1), find_column(input, t.slice[1]))

#/////////////////////////////////////// FOR //////////////////////////////////////////////////
def p_for(t):
    '''
    for_instr : RFOR PARA declasigna PUNTOCOMA expresion PUNTOCOMA actualizacion PARC LLAVEA instrucciones LLAVEC
    '''
    t[0] = For(t[3], t[5], t[7], t[10], t.lineno(1), find_column(input, t.slice[1]))

def p_declasigna(t):
    '''
    declasigna : declaracion_instr
                | asignacion_instr
                |
    '''
    t[0] = t[1]

def p_actualizacion(t):
    '''
    actualizacion : incremento_instr
                    | decremento_instr
                    | asignacion_instr
    '''

    t[0] = t[1]

#///////////////////////////////////////BREAK//////////////////////////////////////////////////

def p_break(t):
    '''break_instr : RBREAK
    '''
    t[0] = Break(t.lineno(1), find_column(input, t.slice[1]))

#///////////////////////////////////////MAIN//////////////////////////////////////////////////

def p_main(t) :
    'main_instr     : RMAIN PARA PARC LLAVEA instrucciones LLAVEC'
    t[0] = Main(t[5], t.lineno(1), find_column(input, t.slice[1]))

#/////////////////////////////////////// INCREMENTO //////////////////////////////////////////////////

def p_incremento(t):
    'incremento_instr : ID MASMAS'
    t[0] = Incremento(t[1], t.lineno(1), find_column(input, t.slice[1]))

#/////////////////////////////////////// DECREMENTO //////////////////////////////////////////////////

def p_decremento(t):
    'decremento_instr : ID MENOSMENOS'
    t[0] = Decremento(t[1], t.lineno(1), find_column(input, t.slice[1]))

#/////////////////////////////////////// TIPO //////////////////////////////////////////////////

def p_tipo(t):
    '''
    tipo : RINT
            | RDOUBLE
            | RBOOLEAN
            | RCHAR
            | RSTRING
    '''
    if t[1].lower() == 'int':
        t[0] = TIPO.ENTERO
    elif t[1].lower() == 'double':
        t[0] = TIPO.DECIMAL
    elif t[1].lower() == 'boolean':
        t[0] = TIPO.BOOLEANO
    elif t[1].lower() == 'char':
        t[0] = TIPO.CHARACTER
    elif t[1].lower() == 'string':
        t[0] = TIPO.CADENA


#///////////////////////////////////////EXPRESION//////////////////////////////////////////////////

def p_expresion_binaria(t):
    '''
    expresion : expresion MAS expresion
            | expresion MENOS expresion
            | expresion POR expresion
            | expresion DIV expresion
            | expresion POTENCIA expresion
            | expresion MODULO  expresion
            | expresion IGUALIGUAL expresion
            | expresion DIFERENTE expresion
            | expresion MENORQUE expresion
            | expresion MAYORQUE expresion
            | expresion MENORIGUAL expresion
            | expresion MAYORIGUAL expresion
            | expresion OR expresion
            | expresion AND expresion
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
    elif t[2] == "==":
        t[0] = Relacional(OperadorRelacional.IGUALIGUAL, t[1], t[3], t.lineno(2), find_column(input, t.slice[2]))
    elif t[2] == "=!":
        t[0] = Relacional(OperadorRelacional.DIFERENTE, t[1], t[3], t.lineno(2), find_column(input, t.slice[2]))
    elif t[2] == "<":
        t[0] = Relacional(OperadorRelacional.MENORQUE, t[1],t[3],t.lineno(2), find_column(input, t.slice[2]))
    elif t[2] == ">":
        t[0] = Relacional(OperadorRelacional.MAYORQUE, t[1],t[3],t.lineno(2), find_column(input, t.slice[2]))
    elif t[2] == "<=":
        t[0] = Relacional(OperadorRelacional.MENORIGUAL, t[1],t[3],t.lineno(2), find_column(input, t.slice[2]))
    elif t[2] == ">=":
        t[0] = Relacional(OperadorRelacional.MAYORIGUAL, t[1],t[3],t.lineno(2), find_column(input, t.slice[2]))
    elif t[2] == "||":
        t[0] = Logica(OperadorLogico.OR, t[1],t[3],t.lineno(2), find_column(input, t.slice[2]))
    elif t[2] == "&&":
        t[0] = Logica(OperadorLogico.AND, t[1],t[3],t.lineno(2), find_column(input, t.slice[2]))
    

'''def p_expresion_error(t):
    'expresion : error'
    errores.append(Excepcion("Sintactico","Error Sintactico." + str(t[1].value) , t.lineno(1), find_column(input, t.slice[1])))
    t[0] = ""
'''
def p_expresion_unaria(t):
    '''
    expresion : MENOS expresion %prec UMENOS
                | NOT expresion %prec UNOT
    '''
    if t[1] == "-":
        t[0] = Aritmetica(OperadorAritmetico.UMENOS, t[2], None, t.lineno(1), find_column(input, t.slice[1]))
    elif t[1] == "!":
        t[0] = Logica(OperadorLogico.NOT, t[2], None, t.lineno(1), find_column(input, t.slice[1]))

#///////////////////////////////////////EXPRESION CASTEO//////////////////////////////////////////////////

def p_expresion_casteo(t):
    'expresion : PARA tipo PARC expresion'
    t[0] = Casteo(t[2], t[4], t.lineno(1), find_column(input, t.slice[1]))

#///////////////////////////////////////EXPRESION INCREMENTO//////////////////////////////////////////////////

def p_expresion_incremento(t):
    'expresion : incremento_instr'
    t[0] = t[1]

#///////////////////////////////////////EXPRESION DECREMENTO //////////////////////////////////////////////////

def p_expresion_decremento(t):
    'expresion : decremento_instr'
    t[0] = t[1]

def p_expresion_agrupacion(t):
    '''
    expresion :   PARA expresion PARC 
    '''
    t[0] = t[2]

def p_expresion_identificador(t):
    '''expresion : ID'''
    t[0] = Identificador(t[1], t.lineno(1), find_column(input, t.slice[1]))

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

def p_nulo(t):
    'expresion : RNULL'
    t[0] = Primitivos(TIPO.NULO, "null",t.lineno(1), find_column(input, t.slice[1]))

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
    lexer = lex.lex(reflags=re.IGNORECASE)
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

    for instruccion in ast.getInstrucciones():      # PRIMERA PASADA (DECLARACIONES Y ASIGNACIONES)
        if isinstance(instruccion, Declaracion) or isinstance(instruccion, Asignacion):
            value = instruccion.interpretar(ast,TSGlobal)
            if isinstance(value, Excepcion) :
                ast.getExcepciones().append(value)
                ast.updateConsola(value.toString())
            if isinstance(value, Break) :
                err = Excepcion("Semantico", "Sentencia BREAK fuera de ciclo.", instruccion.fila, instruccion.columna)
                ast.getExcepciones().append(err)
                ast.updateConsola(err.toString())
        
    for instruccion in ast.getInstrucciones():      # SEGUNDA PASADA (Main)
        contador = 0
        if isinstance(instruccion, Main):
            contador += 1
            if contador == 2: #VERIFICA LA DUPLICIDAD DEL MAIN
                err = Excepcion("Semantico", "Existen 2 funciones main.", instruccion.fila, instruccion.columna)
                ast.getExcepciones().append(err)
                ast.updateConsola(err.toString())
                break
            value = instruccion.interpretar(ast,TSGlobal)
            if isinstance(value, Excepcion) :
                ast.getExcepciones().append(value)
                ast.updateConsola(value.toString())
            if isinstance(value, Break) :
                err = Excepcion("Semantico", "Sentencia BREAK fuera de ciclo.", instruccion.fila, instruccion.columna)
                ast.getExcepciones().append(err)
                ast.updateConsola(err.toString())

    for instruccion in ast.getInstrucciones():
        if not (isinstance(instruccion, Main) or isinstance(instruccion, Declaracion) or isinstance(instruccion, Asignacion)):
                err = Excepcion("Semantico", "Sentencia fuera de main.", instruccion.fila, instruccion.columna)
                ast.getExcepciones().append(err)
                ast.updateConsola(err.toString())



    return ast.getConsola()
