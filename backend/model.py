from __future__ import annotations

context = {}


class Prog:
    def __init__(self, prog: Prog):
        self.prog: Prog = prog

    def __call__(self):
        return self.prog()


class Sum(Prog):
    def __init__(self, var: str, init: Prog, end: Prog, body: Prog):
        self.var = var
        self.init = init
        self.end = end
        self.body = body

    def __call__(self):
        v_init = int(self.init())
        v_end = int(self.end())
        s = 0
        for k in range(v_init, v_end + 1):
            context[self.var] = k
            s += self.body()
        return s


class Value(Prog):
    def __init__(self, value: int):
        self.value = value

    def __call__(self):
        return self.value


class Var(Prog):
    def __init__(self, var: str):
        self.var = var

    def __call__(self):
        return context[self.var]


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
