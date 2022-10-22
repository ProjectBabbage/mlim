from __future__ import annotations

context = {}


class Prog:
    def __init__(self, prog: Prog):
        self.prog: Prog = prog

    def __call__(self):
        return self.prog()


class Value(Prog):
    def __init__(self, value: int):
        self.value = value

    def __call__(self):
        return self.value


class Var(Prog):
    def __init__(self, value: str):
        self.value = value

    def __call__(self):
        return context[self.value]


class BinOp(Prog):
    def __init__(self, left: Prog, op: str, right: Prog):
        self.left = left
        self.op = op
        self.right = right

    def __call__(self):
        if self.op == "+":
            return self.left() + self.right()
        elif self.op == "-":
            return self.left() - self.right()
        elif self.op == "*":
            return self.left() * self.right()
        elif self.op == "/":
            return self.left() / self.right()
