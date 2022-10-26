import ply.yacc as yacc
import model

from lexer import tokens  # noqa: F401

precedence = (
    ("left", "ADDOP"),
    ("left", "MULOP"),
)


def p_program_assign(p):
    "program : VAR SEMICOL func"
    model.State.store[p[1]] = p[3]
    p[0] = p[3]


def p_program_prog(p):
    "program : func"
    p[0] = p[1]


def p_func_function(p):
    "func : VAR MAPSTO prog"
    p[0] = model.Function(p[1], p[3])


def p_func_prog(p):
    "func : prog"
    p[0] = p[1]


def p_prog_addop(p):
    "prog : prog ADDOP prog"
    p[0] = model.BinOp(p[1], p[2], p[3])


def p_prog_sum(p):
    "prog : SUM UNDERS LBRACK VAR EQUALS prog RBRACK CARET LBRACK prog RBRACK mulprog"
    p[0] = model.Sum(p[4], p[6], p[10], p[12])


def p_prog_mulprog(p):
    "prog : mulprog"
    p[0] = p[1]


def p_mulprog_mulop(p):
    "mulprog : mulprog MULOP mulprog"
    p[0] = model.BinOp(p[1], p[2], p[3])


def p_mulprog_mul(p):
    "prog : PRODUCT UNDERS LBRACK VAR EQUALS prog RBRACK CARET LBRACK prog RBRACK mulprog"
    p[0] = model.Product(p[4], p[6], p[10], p[12])


def p_mulprog_lit(p):
    "mulprog : literal"
    p[0] = p[1]


def p_literal_call(p):
    "literal : VAR LPAREN prog RPAREN"
    p[0] = model.Call(p[1], p[3])


def p_literal_paren(p):
    "literal : LPAREN prog RPAREN"
    p[0] = p[2]


def p_literal_nabla(p):
    "literal : NABLA VAR"
    p[0] = model.Nabla(p[2])


def p_literal_var(p):
    "literal : VAR"
    p[0] = model.Var(p[1])


def p_literal_num(p):
    "literal : NUMBER"
    p[0] = model.Value(p[1])


def p_expression_multiline(p):
    "literal : BEGIN LBRACK MULTILINE RBRACK multiline END LBRACK MULTILINE RBRACK"
    p[0] = model.Matrix(p[5])


def p_multiline_line(p):
    """multiline : line DOUBLEBS multiline
    | line"""
    if len(p) == 4:
        p[0] = [p[1]] + p[3]
    elif len(p) == 2:
        p[0] = [p[1]]


def p_line_list(p):
    """line : prog AMPER line
    | prog"""
    if len(p) == 4:
        p[0] = [p[1]] + p[3]
    elif len(p) == 2:
        p[0] = [p[1]]


def p_literal_cell(p):
    "literal : VAR UNDERS LBRACK prog COMMA prog RBRACK"
    p[0] = model.Cell(model.State.store[p[1]], p[4], p[6])


def p_error(p):
    print("Syntax error in line %d" % p.lineno)
    latex_parser.errok()


latex_parser = yacc.yacc(outputdir="parser_generated")
