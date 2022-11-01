import ply.yacc as yacc
from compiler import model

from compiler.lexer import tokens  # noqa: F401

precedence = (
    ("left", "ADDOP"),
    ("left", "MULOP"),
)


def p_program(p):
    """program : VAR SEMICOL func
    | func"""
    if len(p) == 4:
        model.State.store[p[1]] = p[3]
        p[0] = p[3]
    else:
        p[0] = p[1]


def p_func(p):
    """func : VAR MAPSTO prog
    | prog"""
    if len(p) == 4:
        p[0] = model.Function(p[1], p[3])
    else:
        p[0] = p[1]


def p_prog(p):
    """prog : SUM UNDERS LBRACK VAR EQUALS prog RBRACK CARET LBRACK prog RBRACK mulprog
    | prog ADDOP prog
    | mulprog"""
    if len(p) == 13:
        p[0] = model.Sum(p[4], p[6], p[10], p[12])
    elif len(p) == 4:
        p[0] = model.BinOp(p[1], p[2], p[3])
    else:
        p[0] = p[1]


def p_mulprog(p):
    """mulprog : PRODUCT UNDERS LBRACK VAR EQUALS prog RBRACK CARET LBRACK prog RBRACK literal
    | mulprog MULOP mulprog
    | ADDOP prog
    | literal"""
    if len(p) == 13:
        p[0] = model.Product(p[4], p[6], p[10], p[12])
    elif len(p) == 4:
        p[0] = model.BinOp(p[1], p[2], p[3])
    elif len(p) == 3:
        p[0] = model.UnOp(p[1], p[2])
    else:
        p[0] = p[1]


def p_literal(p):
    """literal : BEGIN LBRACK MULTILINE RBRACK multiline END LBRACK MULTILINE RBRACK
    | VAR UNDERS LBRACK prog COMMA prog RBRACK
    | VAR LPAREN prog RPAREN
    | LPAREN prog RPAREN
    | NABLA VAR
    | VAR
    | NUMBER"""
    if len(p) == 10:
        p[0] = model.Matrix(p[5])
    elif len(p) == 8:
        p[0] = model.SelectElement(p[1], p[4], p[6])
    elif len(p) == 5:
        p[0] = model.Call(p[1], p[3])
    elif len(p) == 4:
        p[0] = p[2]
    elif len(p) == 3:
        p[0] = model.GradientDescent(p[2])
    elif len(p) == 2 and isinstance(p[1], float):
        p[0] = model.Value(p[1])
    elif len(p) == 2 and isinstance(p[1], str):
        p[0] = model.Var(p[1])


def p_multiline(p):
    """multiline : line DOUBLEBS multiline
    | line"""
    if len(p) == 4:
        p[0] = [p[1]] + p[3]
    elif len(p) == 2:
        p[0] = [p[1]]


def p_line(p):
    """line : prog AMPER line
    | prog"""
    if len(p) == 4:
        p[0] = [p[1]] + p[3]
    elif len(p) == 2:
        p[0] = [p[1]]


def p_error(p):
    print("Syntax error in line %d" % p.lineno)
    latex_parser.errok()


latex_parser = yacc.yacc(outputdir="compiler/parser_generated")
