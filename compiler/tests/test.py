from pathlib import Path
from unittest import TestCase
from compiler import parser, model


class TestBinOps(TestCase):
    def test_addition(self):
        addition_tex = Path("fixtures/addition.tex").read_text()
        prog = parser.yacc.parse(addition_tex)
        self.assertEqual(prog().operand, 2)

    def test_float(self):
        float_tex = Path("fixtures/float.tex").read_text()
        prog = parser.yacc.parse(float_tex)
        self.assertEqual(prog().operand, -12.43)

    def test_line_of_number_and_binop(self):
        line_of_number_and_binop_tex = Path(
            "fixtures/line_of_number_and_binop.tex"
        ).read_text()
        prog = parser.yacc.parse(line_of_number_and_binop_tex)
        self.assertEqual(prog().operand, 11 + 13 - 123 / 7878 * 122)

    def test_paren_formula(self):
        paren_formula_tex = Path("fixtures/paren_formula.tex").read_text()
        prog = parser.yacc.parse(paren_formula_tex)
        self.assertEqual(prog().operand, 17)


class TestProduct(TestCase):
    def test_simple_product(self):
        simple_product_tex = Path("fixtures/simple_product.tex").read_text()
        prog = parser.yacc.parse(simple_product_tex)
        self.assertEqual(prog().operand, 120)


class TestSum(TestCase):
    def test_simple_sum(self):
        simple_sum_tex = Path("fixtures/simple_sum.tex").read_text()
        prog = parser.yacc.parse(simple_sum_tex)
        self.assertEqual(prog().operand, 55)


class TestMatrix(TestCase):
    def test_bmatrix_1d(self):
        bmatrix_1d_tex = Path("fixtures/bmatrix_1d.tex").read_text()
        prog = parser.yacc.parse(bmatrix_1d_tex)
        self.assertEqual(
            str(prog()),
            "\\begin{bmatrix}1.0\\\\3.0\\\\8.0\\\\2.0\\\\6.0\\\\8.0\\end{bmatrix}",
        )

    def test_bmatrix_2d(self):
        bmatrix_2d_tex = Path("fixtures/bmatrix_2d.tex").read_text()
        prog = parser.yacc.parse(bmatrix_2d_tex)
        self.assertEqual(
            str(prog()), "\\begin{bmatrix}2.0&4.0\\\\3.0&9.0\\\\9.0&2.0\\end{bmatrix}"
        )

    def test_bmatrix_add(self):
        bmatrix_add_tex = Path("fixtures/bmatrix_add.tex").read_text()
        prog = parser.yacc.parse(bmatrix_add_tex)
        self.assertEqual(
            str(prog()), "\\begin{bmatrix}4.0&8.0\\\\6.0&18.0\\\\18.0&8.0\\end{bmatrix}"
        )

    def test_bmatrix_of_binops(self):
        bmatrix_of_binops_tex = Path("fixtures/bmatrix_of_binops.tex").read_text()
        prog = parser.yacc.parse(bmatrix_of_binops_tex)
        self.assertEqual(
            str(prog()),
            "\\begin{bmatrix}1.0&7.5\\\\3.0&5.0\\\\8.0&0.0\\\\2.0&-8.0\\end{bmatrix}",
        )

    def test_bmatrix_mul(self):
        bmatrix_mul_tex = Path("fixtures/bmatrix_mul.tex").read_text()
        prog = parser.yacc.parse(bmatrix_mul_tex)
        self.assertEqual(
            str(prog()),
            "\\begin{bmatrix}24.0&18.0&14.0\\\\51.0&33.0&24.0\\\\23.0&47.0&46.0\\end{bmatrix}",
        )

    def test_bmatrix_of_binops_mul(self):
        bmatrix_of_binops_mul_tex = Path(
            "fixtures/bmatrix_of_binops_mul.tex"
        ).read_text()
        prog = parser.yacc.parse(bmatrix_of_binops_mul_tex)
        self.assertEqual(
            str(prog()),
            "\\begin{bmatrix}24.0&18.0&14.0\\\\51.0&33.0&24.0\\\\23.0&47.0&46.0\\end{bmatrix}",
        )

    def test_bmatrix_formula(self):
        bmatrix_formula_tex = Path("fixtures/bmatrix_formula.tex").read_text()
        prog = parser.yacc.parse(bmatrix_formula_tex)
        self.assertEqual(
            str(prog()), "\\begin{bmatrix}135.8&37.8\\\\71.4&49.0\\end{bmatrix}"
        )


class TestAssignement(TestCase):
    def setUp(self) -> None:
        model.State.store = {}

    def test_assign_value(self):
        assign_value_tex = Path("fixtures/assign_value.tex").read_text()
        prog = parser.yacc.parse(assign_value_tex)
        self.assertEqual(prog().operand, 2)
        self.assertEqual(model.State.store["a"].operand, 2.0)

    def test_assign_function(self):
        assign_function_tex = Path("fixtures/assign_function.tex").read_text()
        prog = parser.yacc.parse(assign_function_tex)
        self.assertEqual(str(prog), "x \\mapsto (x+x)")
        self.assertEqual(str(model.State.store["f"]), "x \\mapsto (x+x)")

    def test_assign_matrix(self):
        assign_matrix_tex = Path("fixtures/assign_matrix.tex").read_text()
        prog = parser.yacc.parse(assign_matrix_tex)
        self.assertEqual(
            str(prog()), "\\begin{bmatrix}2.0&3.0\\\\4.0&1.0\\end{bmatrix}"
        )
        self.assertEqual(
            str(model.State.store["A"]),
            "\\begin{bmatrix}2.0&3.0\\\\4.0&1.0\\end{bmatrix}",
        )

    def test_assign_var(self):
        assign_var_tex = Path("fixtures/assign_var.tex").read_text()
        prog = parser.yacc.parse(assign_var_tex)
        self.assertEqual(str(prog), "(x+2.0)")
        self.assertEqual(str(model.State.store["a"]), "(x+2.0)")


class TestEvaluation(TestCase):
    @classmethod
    def setUpClass(cls):
        model.State.store = {
            "i": model.Value(1.0),
            "A": model.Matrix(
                [
                    [model.Value(6.0), model.Value(7.0)],
                    [model.Value(8.0), model.Value(9.0)],
                ]
            ),
            "f": model.Function("x", model.BinOp(model.Var("x"), "+", model.Var("x"))),
        }

    def test_evaluation_test(self):
        evaluation_test_tex = Path("fixtures/evaluation_test.tex").read_text()
        prog = parser.yacc.parse(evaluation_test_tex)
        self.assertEqual(prog().operand, 8.0)

    def test_evaluation_matrix_cell(self):
        evaluation_matrix_cell_tex = Path(
            "fixtures/evaluation_matrix_cell.tex"
        ).read_text()
        prog = parser.yacc.parse(evaluation_matrix_cell_tex)
        self.assertEqual(prog().operand, 8.0)

    def test_evaluation_function(self):
        evaluation_function_tex = Path("fixtures/evaluation_function.tex").read_text()
        prog = parser.yacc.parse(evaluation_function_tex)
        self.assertEqual(prog().operand, 8.0)

    @classmethod
    def tearDownClass(cls) -> None:
        model.State.store = {}


class TestSimplify(TestCase):
    def test_evaluation_simplify(self):
        evaluation_simplify_tex = Path("fixtures/evaluation_simplify.tex").read_text()
        prog = parser.yacc.parse(evaluation_simplify_tex)
        prog = prog.rewrite()
        self.assertEqual(str(prog()), "y")

    # def test_TEMPLATE(self):
    #     TEMPLATE_tex = Path("fixtures/TEMPLATE.tex").read_text()
    #     prog = parser.yacc.parse(TEMPLATE_tex)
    #     self.assertEqual(prog().operand, XXX)
