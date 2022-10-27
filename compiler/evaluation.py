from compiler import parser
from compiler.model import Value, Matrix


def evaluation(input_tex):
    prog = parser.yacc.parse(input_tex)
    try:
        ret_value = prog()
    except:  # noqa : E712
        ret_value = prog
    return ret_value


if __name__ == "__main__":
    import sys

    input_tex = open(sys.argv[1]).read()
    st = {
        "A": Matrix([[Value(6.0), Value(7.0)], [Value(8.0), Value(9.0)]]),
        "i": Value(1.0),
    }
    print(evaluation(st, input_tex))
