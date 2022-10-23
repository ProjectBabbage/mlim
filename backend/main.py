import parser

if __name__ == "__main__":
    import sys

    input_tex = open(sys.argv[1]).read()
    prog = parser.yacc.parse(input_tex)
    print(prog())
