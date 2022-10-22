import ply.yacc as yacc
import model

from lexer import tokens  # noqa: F401

precedence = (
    ("left", "ADDOP"),
    ("left", "MULOP"),
)

context = {}


def p_prog_addop(p):
    "prog : prog ADDOP prog"
    p[0] = model.Binop(p[1], p[2], p[3])


def p_prog_sum(p):
    "prog : SUM CARET LBRACK VAR EQUALS prog RBRACK"
    p[0] = p[6]
    # "prog : SUM CARET LBRACK VAR EQUALS prog RBRACK UNDERS LBRACK prog RBRACK mulprog"
    # i = p[4]
    # i_initial = p[6]()
    # i_final = p[10]()
    # s = 0
    # for k in range(i_initial, i_final + 1):
    #     context[i] = k
    #     s += p[12]()
    # p[0] = s


def p_prog_mulprog(p):
    "prog : mulprog"
    p[0] = p[1]


def p_mulprog_mulop(p):
    "mulprog : mulprog MULOP mulprog"
    p[0] = model.Binop(p[1], p[2], p[3])


def p_mulprog_lit(p):
    "mulprog : literal"
    p[0] = p[1]


def p_literal_paren(p):
    "literal : LPAREN prog RPAREN"
    p[0] = p[2]


def p_literal_num(p):
    "literal : NUMBER"
    p[0] = p[1]


def p_error(p):
    print("Syntax error in line %d" % p.lineno)
    latex_parser.errok()


latex_parser = yacc.yacc(outputdir="parser_generated")
