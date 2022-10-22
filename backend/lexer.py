import ply.lex as lex

tokens = ("NUMBER", "MULOP", "ADDOP", "LPAREN", "RPAREN", "SUM")

t_LPAREN = r"\("
t_RPAREN = r"\)"

t_ADDOP = r"\+|-"
t_MULOP = r"\*|/"

t_SUM = r"\\sum"


def t_NUMBER(t):
    r"-?\d+(\.\d+)?"
    t.value = float(t.value)
    return t


t_ignore = "\t \n"


def t_error(t):
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)


lex.lex()
