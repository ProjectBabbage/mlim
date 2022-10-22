import numpy as np
import ply.yacc as yacc

from lexer import tokens  # noqa: F401

precedence = (
    ("left", "ADDOP"),
    ("left", "MULOP"),
)


def p_expression_num(p):
    "expression : NUMBER"
    p[0] = p[1]


def p_expression_paren(p):
    "expression : LPAREN expression RPAREN"
    p[0] = p[2]


def p_expression_addop(p):
    "expression : expression ADDOP expression"
    if p[2] == "+":
        p[0] = p[1] + p[3]
    elif p[2] == "-":
        p[0] = p[1] - p[3]


def p_expression_mulop(p):
    "expression : expression MULOP expression"
    if p[2] == "*":
        p[0] = p[1] * p[3]
    elif p[2] == "/":
        p[0] = p[1] / p[3]


def p_expression_multiline(p):
    "expression : BSLASH BEGIN LBRACK MULTILINE RBRACK multiline BSLASH END LBRACK MULTILINE RBRACK"
    if p[4] == "bmatrix":
        p[0] = p[6]


def p_multiline_line(p):
    """multiline : line DOUBLEBS multiline
    | line"""
    if len(p) == 4:
        p[0] = [p[1]] + p[3]
    elif len(p) == 2:
        p[0] = [p[1]]


def p_line_list(p):
    """line : expression AMPER line
    | expression"""
    if len(p) == 4:
        p[0] = [p[1]] + p[3]
    elif len(p) == 2:
        p[0] = [p[1]]


def p_error(p):
    print("Syntax error in line %d" % p.lineno)
    latex_parser.errok()


latex_parser = yacc.yacc(outputdir="parser_generated")
