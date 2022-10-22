import ply.lex as lex

reserved = {
    "begin": "BEGIN",
    "end": "END",
    "bmatrix": "MULTILINE",
}

tokens = [
    "NUMBER",
    "MULOP",
    "ADDOP",
    "CARET",
    "LPAREN",
    "RPAREN",
    "SUM",
    "LBRACK",
    "RBRACK",
    "UNDERS",
    "EQUALS",
    "AMPER",
    "DOUBLEBS",
    "BSLASH",
    "VAR",
] + list(reserved.values())

t_LPAREN = r"\("
t_RPAREN = r"\)"
t_LBRACK = r"\{"
t_RBRACK = r"\}"

t_EQUALS = r"="
t_UNDERS = r"\_"
t_CARET = r"\^"
t_ADDOP = r"\+|-"
t_MULOP = r"\*|/"
t_BSLASH = r"\\"
t_SUM = r"\\sum"

t_DOUBLEBS = r"\\\\"
t_AMPER = r"&"

t_ignore = "\t "


def t_VAR(t):
    r"[a-z]+"
    t.type = reserved.get(t.value, "VAR")
    t.value = str(t.value)
    return t


def t_newline(t):
    r"\n+"
    t.lexer.lineno += len(t.value)


def t_NUMBER(t):
    r"-?\d+(\.\d+)?"
    t.value = float(t.value)
    return t


def t_error(t):
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)


lex.lex()
