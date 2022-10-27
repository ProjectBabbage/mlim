from compiler import parser
from compiler.model import Value, Matrix


def evaluation(input_tex):
    message = ""
    ret_value = ""
    try:
        prog = parser.yacc.parse(input_tex)
        ret_value = prog()
    except TypeError as te:
        print("TypeError", te)
    except KeyError as ke:
        print("KeyError", ke)
    except Exception as e:
        message = str(e)
        print("Exception", e)
    return ret_value, message


if __name__ == "__main__":
    import sys

    input_tex = open(sys.argv[1]).read()
    st = {
        "A": Matrix([[Value(6.0), Value(7.0)], [Value(8.0), Value(9.0)]]),
        "i": Value(1.0),
    }
    print(evaluation(st, input_tex))
