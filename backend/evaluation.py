import parser
from model import State, Value, Matrix


def evaluation(passed_store, input_tex):
    State.store = passed_store
    prog = parser.yacc.parse(input_tex)
    try:
        ret_value = prog()
    except:  # noqa : E712
        ret_value = prog
    passed_store = State.store
    return ret_value


if __name__ == "__main__":
    import sys

    input_tex = open(sys.argv[1]).read()
    st_matrix_cell = {"A": Matrix([[5 + 1, 7], [8, 9]])}
    st = {"i": Value(1.0)}
    print(evaluation(st_matrix_cell, input_tex))
