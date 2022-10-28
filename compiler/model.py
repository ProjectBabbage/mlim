from __future__ import annotations
from typing import List
from compiler import utils, gradient_descent


class State:
    store = {}
    cells = []
    context = {}


class Prog:
    def __init__(self, prog: Prog):
        self.prog: Prog = prog

    def __call__(self):
        return self.prog()


class Function:
    def __init__(self, var: str, prog: Prog):
        self.var = var
        self.prog = prog

    def __call__(self, value: float):
        if self.var in State.context:
            raise EnvironmentError
        State.context[self.var] = value
        ret_value = self.prog()
        del State.context[self.var]
        return ret_value


class Call:
    def __init__(self, func: str, arg: Prog):
        self.func = func
        self.arg = arg

    def __call__(self):
        f = State.store[self.func]
        return f(self.arg())


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
    def __init__(self, value):
        self.value = value

    def __call__(self):
        return self.value

    def __add__(self, b):
        return Value(self.value + b.value)

    def __sub__(self, b):
        self.value -= b.value
        return self

    def __mul__(self, b):
        print(self.value, " : ", b.value)
        self.value = self.value * b.value
        return self

    def __truediv__(self, b):
        self.value /= b.value
        return self

    def __repr__(self):
        return "Value: " + str(self.value)


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
        return Matrix([[Value(x()) for x in line] for line in self.matrix])

    def __mul__(self, b):
        return utils.mulMatrix(self.matrix, b.matrix)

    def __add__(self, b):
        return utils.addMatrix(self.matrix, b.matrix)

    def __repr__(self):
        return "Matrix: " + str(self.matrix)


class SelectElement(Prog):
    def __init__(self, var: Matrix, i: Prog, j: Prog):
        self.var = var
        self.i = i
        self.j = j

    def __call__(self):
        return utils.selectElement(self.var.matrix, self.i(), self.j())()


class BinOp(Prog):
    def __init__(self, left: Prog, op: str, right: Prog):
        self.left = left
        self.op = op
        self.right = right

    def __call__(self):
        # we try to calculate first the subprograms, avoids useless calculation later
        left = self.left()
        right = self.right()
        print(left, right)
        if self.op == "+":
            return left + right
        elif self.op == "-":
            return left - right
        elif self.op == "*":
            if type(right) == Matrix and type(left) == float:
                return utils.mulMatrixbyScalar(right.matrix, left)
            elif type(left) == Matrix and type(right) == float:
                return utils.mulMatrixbyScalar(left.matrix, right)
            return left * right
        elif self.op == "/":
            if type(left) == Matrix and type(right) == float:
                return utils.divMatrixbyScalar(left.matrix, right)
            return left / right


class SingleOp(Prog):
    def __init__(self, op: str, right: Prog):
        self.op = op
        self.right = right

    def __call__(self):
        right = self.right()
        if self.op == "+":
            return right
        elif self.op == "-":
            if type(right) == Matrix:
                return utils.mulMatrixbyScalar(right.matrix, -1)
            return -1 * right


class GradientDescent(Prog):
    def __init__(self, var: str):
        self.var = var

    def __call__(self):
        return gradient_descent.wrapper(State.store[self.var])
