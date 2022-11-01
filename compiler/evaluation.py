from compiler import parser
from compiler.model import Value, Matrix, State


def evaluation(input_tex):
    message = ""
    ret_value = ""
    try:
        prog = parser.yacc.parse(input_tex)
        ret_value = str(prog())
    except TypeError as te:
        print("TypeError", te)
    except KeyError as ke:
        ret_value = str(prog)
        print("KeyError", ke)
    except Exception as e:
        message = str(e)
        print("Exception", e)
    return ret_value, message
