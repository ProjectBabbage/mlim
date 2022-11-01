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
            # Because types are either value or matrix, s cannot be set prior
            if k == v_init:
                s = self.body()
            else:
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
            # Because types are either value or matrix, s cannot be set prior
            State.context[self.var] = k
            if k == v_init:
                s = self.body()
            else:
                s *= self.body()
        return s


class Var(Prog):
    def __init__(self, var: str):
        self.var = var

    def __call__(self):
        if self.var in State.context:
            return State.context[self.var]
        else:
            return State.store[self.var]()


class Operand(Prog):
    def __init__(self, operand):
        self.operand = operand

    def __call__(self):
        return self


class Value(Operand):
    def __init__(self, operand: float):
        super().__init__(operand)

    def __add__(self, b):
        return Value(self.operand + b.operand)

    def __sub__(self, b):
        return Value(self.operand - b.operand)

    def __mul__(self, b):
        return Value(self.operand * b.operand)

    def __truediv__(self, b):
        return Value(self.operand / b.operand)


class Matrix(Operand):
    def __init__(self, operand: List[List[Prog]]):
        super().__init__(operand)

    def __call__(self):
        return Matrix([[x() for x in line] for line in self.operand])

    def __mul__(self, b):
        return Matrix(utils.mulMatrix(self.operand, b.operand))

    def __add__(self, b):
        return Matrix(utils.addMatrix(self.operand, b.operand))

    def __sub__(self, b):
        return Matrix(utils.subMatrix(self.operand, b.operand))


class SelectElement(Prog):
    def __init__(self, var: Prog, i: Prog, j: Prog):
        self.var = var
        self.i = i
        self.j = j

    def __call__(self):
        return utils.selectElement(
            self.var().operand, self.i().operand, self.j().operand
        )


class BinOp(Prog):
    def __init__(self, left: Prog, op: str, right: Prog):
        self.left = left
        self.op = op
        self.right = right

    def __call__(self):
        # we try to calculate first the subprograms, avoids useless calculation later
        left = self.left()
        right = self.right()
        if self.op == "+":
            return left + right
        elif self.op == "-":
            return left - right
        elif self.op == "*":
            if type(right) == Matrix and type(left) == Value:
                return utils.mulMatrixbyScalar(right.operand, left.operand)
            elif type(left) == Matrix and type(right) == Value:
                return utils.mulMatrixbyScalar(left.operand, right.operand)
            return left * right
        elif self.op == "/":
            if type(left) == Matrix and type(right) == Value:
                return utils.divMatrixbyScalar(left.operand, right.operand)
            return left / right


class GradientDescent(Prog):
    def __init__(self, var: str):
        self.var = var

    def __call__(self):
        return gradient_descent.wrapper(State.store[self.var])
