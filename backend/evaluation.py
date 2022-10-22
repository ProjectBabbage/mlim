import parser
from model import State


def evaluation(passed_store, prog):
    State.store = passed_store
    ret_value = prog()
    passed_store = State.store
    return ret_value


if __name__ == "__main__":
    import sys

    prog = open(sys.argv[1]).read()
    result = parser.yacc.parse(prog)
    st = {"i": 3}
    print(evaluation(st, result))
