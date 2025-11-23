"""表达式树相关"""
from abc import ABC, abstractmethod
import math


class Node(ABC):
    prio: int  # 运算符优先级，越高表示越先计算

    def __init__(self, prio: int):
        self.prio = prio

    @abstractmethod
    def calc(self) -> float:
        ...

    @abstractmethod
    def __str__(self) -> str:
        """转换为 Latex 表达式"""
        ...


def _br(node: Node, target_prio: int) -> str:
    """在必要时添加括号"""
    if node.prio < target_prio:
        return f"\\left({node}\\right)"
    else:
        return str(node)


class Value(Node):
    """单个数字节点，应作为叶子节点"""
    value: int | float | str

    def __init__(self, value: int | float | str):
        super().__init__(100)
        self.value = value

    def calc(self) -> float:
        if isinstance(self.value, str):
            if self.value == "e":
                return math.e
            elif self.value == "pi":
                return math.pi
            else:
                raise ValueError(f"Unknown value: {self.value}")
        return self.value

    def is_num(self) -> bool:
        return isinstance(self.value, (int, float))

    def __str__(self) -> str:
        if self.value == "e":
            return "\\text{e}"
        elif self.value == "pi":
            return "\\pi"
        return str(self.value)


class BinOp(Node):
    left: Node
    right: Node

    def __init__(self, left: Node, right: Node, prio: int):
        super().__init__(prio)
        self.left = left
        self.right = right


class Add(BinOp):
    def __init__(self, left: Node, right: Node):
        super().__init__(left, right, 1)

    def calc(self) -> float:
        return self.left.calc() + self.right.calc()

    def __str__(self) -> str:
        return f"{_br(self.left, self.prio)} + {_br(self.right, self.prio)}"


class Sub(BinOp):
    def __init__(self, left: Node, right: Node):
        super().__init__(left, right, 1)

    def calc(self) -> float:
        return self.left.calc() - self.right.calc()

    def __str__(self) -> str:
        return f"{_br(self.left, self.prio)} - {_br(self.right, self.prio)}"


class Mul(BinOp):
    def __init__(self, left: Node, right: Node):
        super().__init__(left, right, 2)

    def calc(self) -> float:
        return self.left.calc() * self.right.calc()

    def __str__(self) -> str:
        p = self.right
        while isinstance(p, Pow) or isinstance(p, Mul):
            p = p.left
        cross_mul = (isinstance(p, Value) and p.is_num()  # 两数相乘用乘号
            or (isinstance(p, Div) and isinstance(p.left, Value) and isinstance(p.right, Value))) # 避免和带分数混淆
        if cross_mul:
            return f"{_br(self.left, self.prio)} \\times {self.right}"
        else:
            return f"{_br(self.left, self.prio)} {_br(self.right, self.prio)}"


class Div(BinOp):
    def __init__(self, left: Node, right: Node):
        super().__init__(left, right, 2)

    def calc(self) -> float:
        return self.left.calc() / self.right.calc()

    def __str__(self) -> str:
        return f"\\frac{{{self.left}}}{{{self.right}}}"


class Pow(BinOp):
    def __init__(self, base: Node, exp: Node):
        super().__init__(base, exp, 4)

    def calc(self) -> float:
        return self.left.calc() ** self.right.calc()

    def __str__(self) -> str:
        if isinstance(self.left, Log):
            return f"{self.left.func_name()}^{{{self.right}}}{{{_br(self.left.right, 3)}}}"
        return f"{{{_br(self.left, 5)}}} ^ {{{self.right}}}"


class Log(BinOp):
    def __init__(self, base: Node, arg: Node):
        super().__init__(base, arg, 3)

    def calc(self) -> float:
        return math.log(self.right.calc(), self.left.calc())

    def func_name(self) -> str:
        if isinstance(self.left, Value):
            if self.left.value == 10:
                return "\\lg"
            elif self.left.value == "e":
                return "\\ln"
        return f"\\log_{{{_br(self.left, 5)}}}"

    def __str__(self) -> str:
        return f"{self.func_name()}{{{_br(self.right, 3)}}}"
