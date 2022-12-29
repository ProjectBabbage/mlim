from compiler import parser, lexer
from compiler.model import State


def evaluation(input_tex):
    lexer.reset()
    State.reset_context()
    message = ""
    ret_value = ""
    try:
        prog = parser.yacc.parse(input_tex)
        if State.store["MLIMrewrite"] == 1:
            # try should not be necessary here rewrite must always work
            prog = prog.rewrite()
        ret_value = str(prog())
    except TypeError as te:
        ret_value = str(prog)
        print("TypeError", te)
    except KeyError as ke:
        ret_value = str(prog)
        print("KeyError", ke)
    except Exception as e:
        message = str(e)
        print("Exception", e)
    return ret_value, message


if __name__ == "__main__":
    import sys

    input_tex = open(sys.argv[1]).read()

    print(evaluation(input_tex))
