# chaos.py
from random import choice, randint, random
from typing import List
import expr


def make_chaos(node: expr.Node, depth: int = 0, max_depth: int = 3) -> expr.Node:
    """
    将表达式复杂化
    depth: 当前递归深度
    max_depth: 最大递归深度，控制复杂度
    """
    if depth >= max_depth:
        return node

    # 随机选择一种复杂化策略
    strategies = [
        _apply_log_addition_rule,
        _apply_log_subtraction_rule,
        _apply_power_rule,
        _apply_change_of_base,
        _split_numeric_coefficient,
        _introduce_identity_operations
    ]

    strategy = choice(strategies)
    return strategy(node, depth, max_depth)


def _apply_log_addition_rule(node: expr.Node, depth: int, max_depth: int) -> expr.Node:
    """应用对数加法法则：log_a(b) = log_a(b*c) - log_a(c)"""
    if isinstance(node, expr.Log):
        # 生成一个合适的乘数c
        base = node.left
        arg = node.right

        # 选择乘数策略
        if random() < 0.7:
            # 策略1：使用底数的幂次
            k = randint(1, 3)
            multiplier = expr.Pow(base, expr.Value(k))
        else:
            # 策略2：使用简单数字
            multiplier = expr.Value(choice([2, 3, 4, 5]))

        new_arg = expr.Mul(arg, multiplier)
        log1 = expr.Log(base, new_arg)
        log2 = expr.Log(base, multiplier)

        return expr.Sub(log1, log2)
    return node


def _apply_log_subtraction_rule(node: expr.Node, depth: int, max_depth: int) -> expr.Node:
    """应用对数减法法则：log_a(b) = log_a(b/c) + log_a(c)"""
    if isinstance(node, expr.Log):
        base = node.left
        arg = node.right

        if random() < 0.7:
            divisor = expr.Pow(base, expr.Value(randint(1, 3)))
        else:
            divisor = expr.Value(choice([2, 3, 4, 5]))

        new_arg = expr.Div(arg, divisor)
        log1 = expr.Log(base, new_arg)
        log2 = expr.Log(base, divisor)

        return expr.Add(log1, log2)
    return node


def _apply_power_rule(node: expr.Node, depth: int, max_depth: int) -> expr.Node:
    """应用幂法则：log_a(b) = (1/k) * log_a(b^k)"""
    if isinstance(node, expr.Log):
        k = randint(2, 4)
        base = node.left
        arg = node.right

        new_arg = expr.Pow(arg, expr.Value(k))
        inner_log = expr.Log(base, new_arg)

        return expr.Mul(expr.Div(expr.Value(1), expr.Value(k)), inner_log)
    return node


def _apply_change_of_base(node: expr.Node, depth: int, max_depth: int) -> expr.Node:
    """应用换底公式"""
    if isinstance(node, expr.Log):
        old_base = node.left
        arg = node.right

        new_base = choice([
            expr.Value(2),
            expr.Value(3),
            expr.Value(5),
            expr.Value(10),
            expr.Value('e'),
            expr.Pow(expr.Value(2), expr.Value(2)),  # 2^2
            expr.Pow(expr.Value(3), expr.Value(2))   # 3^2
        ])

        numerator = expr.Log(new_base, arg)
        denominator = expr.Log(new_base, old_base)

        return expr.Div(numerator, denominator)
    return node


def _split_numeric_coefficient(node: expr.Node, depth: int, max_depth: int) -> expr.Node:
    """拆分数值系数：k = m + n 或 k = m * n"""
    if isinstance(node, expr.Value) and isinstance(node.value, int) and node.value > 1:
        if random() < 0.5:
            # 加法拆分
            m = randint(1, node.value - 1)
            n = node.value - m
            return expr.Add(expr.Value(m), expr.Value(n))
        else:
            # 乘法拆分
            # 寻找因子
            factors = [i for i in range(2, node.value) if node.value % i == 0]
            if factors:
                m = choice(factors)
                n = node.value // m
                return expr.Mul(expr.Value(m), expr.Value(n))
    return node


def _introduce_identity_operations(node: expr.Node, depth: int, max_depth: int) -> expr.Node:
    """引入恒等运算：乘以1，加0等"""
    if isinstance(node, (expr.Add, expr.Sub, expr.Mul, expr.Div)):
        # 对子节点递归应用复杂化
        node.left = make_chaos(node.left, depth + 1, max_depth)
        node.right = make_chaos(node.right, depth + 1, max_depth)

    # 在适当位置引入恒等运算
    if random() < 0.5:
        if isinstance(node, expr.Mul):
            # 乘以1的某种形式
            one_forms: List[expr.Node] = [
                expr.Value(1),
                expr.Div(expr.Value(2), expr.Value(2)),
                expr.Pow(expr.Value(1), expr.Value(randint(2, 5))),
                expr.Log(expr.Value(2), expr.Value(2))
            ]
            return expr.Mul(node, choice(one_forms))
        elif isinstance(node, expr.Add):
            # 加0的某种形式
            zero_forms: List[expr.Node] = [
                expr.Value(0),
                expr.Sub(expr.Value(2), expr.Value(2)),
                expr.Mul(expr.Value(0), expr.Value(randint(2, 5)))
            ]
            return expr.Add(node, choice(zero_forms))

    return node
