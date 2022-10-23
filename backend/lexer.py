import ply.lex as lex

reserved = {
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
    "PRODUCT",
    "LBRACK",
    "RBRACK",
    "UNDERS",
    "EQUALS",
    "AMPER",
    "DOUBLEBS",
    "VAR",
    "SEMICOL",
    "BEGIN",
    "END",
] + list(reserved.values())

t_LPAREN = r"\("
t_RPAREN = r"\)"
t_LBRACK = r"\{"
t_RBRACK = r"\}"

t_SEMICOL = r":"
t_EQUALS = r"="
t_UNDERS = r"\_"
t_CARET = r"\^"
t_ADDOP = r"\+|-"
t_MULOP = r"\*|/"
t_SUM = r"\\sum"
t_PRODUCT = r"\\prod"

t_BEGIN = r"\\begin"
t_END = r"\\end"

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


if __name__ == "__main__":
    import sys

    input_tex = open(sys.argv[1]).read()

    lex.input(input_tex)

    while 1:
        tok = lex.token()
        if not tok:
            break
        print("line %d : %s (% s)" % (tok.lineno, tok.type, tok.value))
