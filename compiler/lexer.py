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
    "COMMA",
    "EQUALS",
    "AMPER",
    "DOUBLEBS",
    "VAR",
    "SEMICOL",
    "BEGIN",
    "END",
    "MAPSTO",
    "NABLA",
] + list(reserved.values())

t_LPAREN = r"\("
t_RPAREN = r"\)"
t_LBRACK = r"\{"
t_RBRACK = r"\}"

t_SEMICOL = r":"
t_EQUALS = r"="
t_UNDERS = r"\_"
t_COMMA = r","
t_CARET = r"\^"
t_ADDOP = r"\+|-"
t_MULOP = r"\*|/"
t_SUM = r"\\sum"
t_PRODUCT = r"\\prod"
t_MAPSTO = r"\\mapsto"
t_NABLA = r"\\nabla"

t_BEGIN = r"\\begin"
t_END = r"\\end"

t_DOUBLEBS = r"\\\\"
t_AMPER = r"&"

t_ignore = "\t "


def t_VAR(t):
    r"[a-zA-Z]+"
    t.type = reserved.get(t.value, "VAR")
    t.value = str(t.value)
    return t


def t_newline(t):
    r"\n+"
    t.lexer.lineno += len(t.value)
    t.lexer.offset = t.lexpos + len(t.value)


def t_NUMBER(t):
    r"\d+(\.\d+)?"
    t.value = float(t.value)
    return t


def t_error(t):
    column = t.lexpos - t.lexer.offset + 1
    raise Exception(f"Illegal character '{t.value[0]}' at Ln {t.lineno}, Col {column}")


lexer = lex.lex()
lexer.offset = 0


if __name__ == "__main__":
    import sys

    input_tex = open(sys.argv[1]).read()

    lex.input(input_tex)

    while 1:
        tok = lex.token()
        if not tok:
            break
        print("line %d : %s (% s)" % (tok.lineno, tok.type, tok.value))
