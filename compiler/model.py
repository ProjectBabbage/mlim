from __future__ import annotations
from typing import List
from compiler import utils, gradient_descent


class State:
    defaults = {"MLIMrewrite": 0}
    store = defaults
    cells = []
    context = {}

    @staticmethod
    def reset_context():
        State.context = {}

    @staticmethod
    def restart():
        State.store = {}


class Prog:
    def __init__(self, prog: Prog):
        self.prog: Prog = prog

    def __call__(self):
        return self.prog()

    def rewrite(self):
        if hasattr(self, "prog"):
            return self.prog.rewrite()
        return self


class Function:
    def __init__(self, var: str, prog: Prog):
        self.var = var
        self.prog = prog

    def __call__(self, value: Value):
        if self.var in State.context:
            raise EnvironmentError
        State.context[self.var] = value
        ret_value = self.prog()
        del State.context[self.var]
        return ret_value

    def __str__(self) -> str:
        return self.var + " \mapsto " + str(self.prog)

    def __repr__(self) -> str:
        return "Function: " + self.var


class Call:
    def __init__(self, func: str, arg: Prog):
        self.func = func
        self.arg = arg

    def __call__(self):
        f = State.store[self.func]
        return f(self.arg())

    def __str__(self) -> str:
        return self.func + "(" + str(self.arg) + ")"

    def __repr__(self) -> str:
        return "Call: " + self.func + "(x)"


class Sum(Prog):
    def __init__(self, var: str, init: Prog, end: Prog, body: Prog):
        self.var = var
        self.init = init
        self.end = end
        self.body = body

    def __call__(self):
        v_init = int(self.init().operand)
        v_end = int(self.end().operand)
        s = 0
        for k in range(v_init, v_end + 1):
            State.context[self.var] = Value(k)
            # Because types are either value or matrix, s cannot be set prior
            if k == v_init:
                s = self.body()
            else:
                s += self.body()
        return s

    def __str__(self) -> str:
        return (
            "\\sum_{"
            + self.var
            + "="
            + str(self.init)
            + "}^{"
            + str(self.end)
            + "} "
            + str(self.body)
        )

    def __repr__(self) -> str:
        return "Sum: " + self.var


class Product(Prog):
    def __init__(self, var: str, init: Prog, end: Prog, body: Prog):
        self.var = var
        self.init = init
        self.end = end
        self.body = body

    def __call__(self):
        v_init = int(self.init().operand)
        v_end = int(self.end().operand)
        s = 1
        for k in range(v_init, v_end + 1):
            # Because types are either value or matrix, s cannot be set prior
            State.context[self.var] = Value(k)
            if k == v_init:
                s = self.body()
            else:
                s *= self.body()
        return s

    def __str__(self) -> str:
        return (
            "\\prod_{"
            + self.var
            + "="
            + str(self.init)
            + "}^{"
            + str(self.end)
            + "} "
            + str(self.body)
        )

    def __repr__(self) -> str:
        return "Product: " + self.var


class Var(Prog):
    def __init__(self, var: str):
        self.var = var

    def __call__(self):
        if self.var in State.context:
            return State.context[self.var]
        else:
            return State.store[self.var]()

    def __str__(self) -> str:
        return self.var

    def __repr__(self) -> str:
        return "Var: " + self.var


class Operand(Prog):
    def __init__(self, operand):
        self.operand = operand

    def __call__(self):
        return self

    def __repr__(self) -> str:
        return "Operand:" + str(self.operand)


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

    def __str__(self) -> str:
        return str(self.operand)

    def __repr__(self) -> str:
        return "Value: " + str(self)


class Matrix(Operand):
    def __init__(self, operand: List[List[Prog]]):
        super().__init__(operand)

    def __call__(self):
        return Matrix([[x() for x in line] for line in self.operand])

    def rewrite(self):
        return Matrix([[x.rewrite() for x in line] for line in self.operand])

    def __mul__(self, b):
        return Matrix(utils.mulMatrix(self.operand, b.operand))

    def __add__(self, b):
        return Matrix(utils.addMatrix(self.operand, b.operand))

    def __sub__(self, b):
        return Matrix(utils.subMatrix(self.operand, b.operand))

    def __str__(self) -> str:
        matrix = "\\\\".join("&".join(str(e) for e in line) for line in self.operand)
        return "\\begin{bmatrix}" + matrix + "\\end{bmatrix}"

    def __repr__(self) -> str:
        return "Matrix: " + str(self.operand)


class SelectElement(Prog):
    def __init__(self, var: str, i: Prog, j: Prog):
        self.var = var
        self.i = i
        self.j = j

    def __call__(self):

        return utils.selectElement(
            State.store[self.var]().operand, self.i().operand, self.j().operand
        )

    def __str__(self) -> str:
        return str(self.var) + "_{" + str(self.i) + "," + str(self.j) + "}"

    def __repr__(self) -> str:
        return "Element: " + str(self.var)


class BinOp(Prog):
    def __init__(self, left: Prog, op: str, right: Prog):
        self.left = left
        self.op = op
        self.right = right

    def __call__(self):
        left = self.left()
        right = self.right()
        if self.op == "+":
            return left + right
        elif self.op == "-":
            return left - right
        elif self.op == "*":
            if type(right) == Matrix and type(left) == Value:
                return Matrix(utils.mulMatrixbyScalar(right.operand, left.operand))
            elif type(left) == Matrix and type(right) == Value:
                return Matrix(utils.mulMatrixbyScalar(left.operand, right.operand))
            return left * right
        elif self.op == "/":
            if type(left) == Matrix and type(right) == Value:
                return Matrix(utils.divMatrixbyScalar(left.operand, right.operand))
            return left / right

    def rewrite(self):
        self.left = self.left.rewrite()
        self.right = self.right.rewrite()
        if type(self.left) == Value:
            if type(self.right) == Value:
                return self()
            elif self.left.operand == 0 and self.op == "*":
                return self.left
            elif (self.left.operand == 1 and self.op == "*") or (
                self.left.operand == 0 and self.op in ["+", "-"]
            ):
                return self.right
        elif type(self.right) == Value:
            if self.right.operand == 0 and self.op == "*":
                return self.right
            elif (self.right.operand == 1 and self.op == "*") or (
                self.right.operand == 0 and self.op in ["+", "-"]
            ):
                return self.left
        return self

    def __str__(self) -> str:
        return "(" + str(self.left) + self.op + str(self.right) + ")"

    def __repr__(self) -> str:
        return "Binop: " + str(self.left) + self.op + str(self.right)


class UnOp(Prog):
    def __init__(self, op: str, right: Prog):
        self.op = op
        self.right = right

    def __call__(self):
        right = self.right()
        if self.op == "+":
            return right
        elif self.op == "-":
            if type(right) == Matrix:
                return Matrix(utils.mulMatrixbyScalar(right.operand, -1))
            return Value(-1) * right

    def rewrite(self):
        self.right = self.right.rewrite()
        if type(self.right) == Value:
            if self.op == "+":
                return self.right
            elif self.op == "-":
                return Value(-1) * self.right
        return self


class GradientDescent(Prog):
    def __init__(self, var: str):
        self.var = var

    def __call__(self):
        return gradient_descent.wrapper(State.store[self.var])

    def __str__(self) -> str:
        return "\\nabla " + self.var

    def __repr__(self) -> str:
        return "Grad Desc: " + self.var
