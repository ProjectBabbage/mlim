from __future__ import annotations
from typing import List


class State:
    store = {}
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
            State.context[self.var] = k
            s += self.body()
        return s


class Product(Prog):
    def __init__(self, var: str, init: Prog, end: Prog, body: Prog):
        self.var = var
        self.init = init
        self.end = end
        self.body = body

    def __call__(self):
        v_init = int(self.init())
        v_end = int(self.end())
        s = 1
        for k in range(v_init, v_end + 1):
            State.context[self.var] = k
            s *= self.body()
        return s


class Value(Prog):
    def __init__(self, value: float):
        self.value = value

    def __call__(self):
        return self.value


class Var(Prog):
    def __init__(self, var: str):
        self.var = var

    def __call__(self):
        if self.var in State.context:
            return State.context[self.var]
        else:
            return State.store[self.var]()


class Matrix(Prog):
    def __init__(self, matrix: List[List[Prog]]):
        self.matrix = matrix

    def __call__(self):
        return [[x() for x in line] for line in self.matrix]


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
