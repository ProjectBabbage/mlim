import ply.lex as lex

tokens = (
    'NUMBER',
    'BINOP',
    'LPAREN',
    'RPAREN'
)

t_LPAREN = r'\('
t_RPAREN = r'\)'

t_BINOP  = r'\+|-|\*|/'

def t_NUMBER(t):
    r'\d+'
    t.value = int(t.value)
    return t

t_ignore = '\t \n'

def t_error(t) :
    print ("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)

lex.lex()
