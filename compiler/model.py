from __future__ import annotations
from typing import List
from compiler import utils, gradient_descent


class State:
    store = {}
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
        return f"{self.var} \mapsto {self.prog}"

    def __repr__(self) -> str:
        return f"Function({self.var}, {repr(self.prog)}"


class Call:
    def __init__(self, func: str, arg: Prog):
        self.func = func
        self.arg = arg

    def __call__(self):
        f = State.store[self.func]
        return f(self.arg())

    def __str__(self) -> str:
        return f"{self.func}({self.arg})"

    def __repr__(self) -> str:
        return f"{self.func}({repr(self.arg)})"


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
        return f"\\sum{{{self.var}={self.init}}}^{{{self.end}}} {self.body}"

    def __repr__(self) -> str:
        init = repr(self.init)
        end = repr(self.end)
        body = repr(self.body)
        return f"Sum({self.var}, {init}, {end}, {body})"


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
        return f"\\prod_{{{self.var}={self.init}}}^{{{self.end}}} {self.body}"

    def __repr__(self) -> str:
        init = repr(self.init)
        end = repr(self.end)
        body = repr(self.body)
        return f"Product({self.var}, {init}, {end}, {body})"


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
        return f"Var({self.var})"


class Operand(Prog):
    def __init__(self, operand):
        self.operand = operand

    def __call__(self):
        return self

    def __repr__(self) -> str:
        return f"Operand({repr(self.operand)})"


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
        return f"Value({self.operand})"


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

    def __str__(self) -> str:
        matrix = "\\\\".join("&".join(str(e) for e in line) for line in self.operand)
        return "\\begin{bmatrix}" + matrix + "\\end{bmatrix}"

    def __repr__(self) -> str:
        m = repr(self.operand)
        return f"Matrix({m})"


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
        return f"{self.var}_{{{self.i}, {self.j}}}"

    def __repr__(self) -> str:
        i = repr(self.i)
        j = repr(self.j)
        return f"Select({self.var}, {i}, {j})"


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

    def __str__(self) -> str:
        return f"({self.left}{self.op}{self.right})"

    def __repr__(self) -> str:
        left = repr(self.left)
        right = repr(self.right)
        return f"Binop({self.op}, {left}, {right})"


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

    def __str__(self) -> str:
        return f"{self.op}{self.right}"

    def __repr__(self) -> str:
        return f"Unop({repr(self.op)}, {repr(self.right)})"


class GradientDescent(Prog):
    def __init__(self, var: str):
        self.var = var

    def __call__(self):
        return gradient_descent.wrapper(State.store[self.var])

    def __str__(self) -> str:
        return f"\\nabla {self.var}"

    def __repr__(self) -> str:
        return "GradDesc({repr(self.var)})"
