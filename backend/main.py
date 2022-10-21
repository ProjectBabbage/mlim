import lexer

if __name__ == "__main__":
    import sys
    prog = open(sys.argv[1]).read()

    lexer.lex.input(prog)

    lexer.machin()

    while 1:
        tok = lexer.lex.token()
        if not tok:
             break
        print ("line %d : %s (% s)" % (tok.lineno, tok.type, tok.value))
