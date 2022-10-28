from pathlib import Path
from unittest import TestCase
from compiler import parser


class TestBinOps(TestCase):
    def test_addition(self):
        addition_tex = Path("compiler/tests/fixtures/addition.tex").read_text()
        prog = parser.yacc.parse(addition_tex)
        self.assertEqual(prog(), 2)

    def test_simple_product(self):
        simple_product_tex = Path(
            "compiler/tests/fixtures/simple_product.tex"
        ).read_text()
        prog = parser.yacc.parse(simple_product_tex)
        self.assertEqual(prog(), 120)
