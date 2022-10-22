import parser
from model import State


def evaluation(passed_store, file):
    State.store = passed_store
    ret_value = parser.yacc.parse(file)()
    passed_store = State.store
    return ret_value


if __name__ == "__main__":
    import sys

    file = open(sys.argv[1]).read()
    st = {"i": 3}
    print(evaluation(st, file))
