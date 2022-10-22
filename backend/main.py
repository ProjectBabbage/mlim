import parser

if __name__ == "__main__":
    import sys

    prog = open(sys.argv[1]).read()
    result = parser.yacc.parse(prog)
    print(result)
