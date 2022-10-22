import numpy as np
import ply.yacc as yacc

from lexer import tokens  # noqa: F401


def p_expression_num(p):
    "expression : NUMBER"
    p[0] = p[1]


def p_expression_addop(p):
    "expression : expression ADDOP expression"
    if p[2] == "\+":
        p[0] = p[1] + p[3]
    elif p[2] == "-":
        p[0] = p[1] - p[3]
    elif p[2] == "\*":
        p[0] = p[1] * p[3]
    elif p[2] == "\/":
        p[0] = p[1] / p[3]


def p_error(p):
    print("Syntax error in line %d" % p.lineno)
    latex_parser.errok()


latex_parser = yacc.yacc(outputdir="parser_generated")
