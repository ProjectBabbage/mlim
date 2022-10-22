import parser

if __name__ == "__main__":
    import sys

    file = open(sys.argv[1]).read()
    prog = parser.yacc.parse(file)
    print(prog())
