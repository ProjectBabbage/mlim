import ply.lex as lex

tokens = (
    'NUMBER',
    'PLUS',
    'MINUS'
)

t_PLUS  = r'\+'
t_MINUS = r'-'

def t_NUMBER(t):
    r'\d+'
    t.value = int(t.value)
    return t

t_ignore = '\t '

def t_error(t) :
    print ("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)

lex.lex()

def machin():
    print("tructruc")
