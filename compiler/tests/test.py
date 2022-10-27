from pathlib import Path
from unittest import TestCase
from compiler import parser


class TestSomething(TestCase):
    def test_addition(self):
        addition_tex = Path("compiler/tests/fixtures/addition.tex").read_text()
        prog = parser.yacc.parse(addition_tex)
        self.assertEqual(prog(), 2)
