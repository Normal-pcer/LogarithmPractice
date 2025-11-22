# chaos.py
from random import choice, randint, random
from typing import List, Union
import expr


def make_chaos(node: expr.Node, depth: int = 0, max_depth: int = 4) -> expr.Node:
    """
    将表达式复杂化 - 专注于对数变换
    depth: 当前递归深度
    max_depth: 最大递归深度，控制复杂度
    """
    if depth >= max_depth:
        return node

    # 先对子节点递归应用复杂化
    if hasattr(node, 'left') and node.left is not None:
        node.left = make_chaos(node.left, depth + 1, max_depth)
    if hasattr(node, 'right') and node.right is not None:
        node.right = make_chaos(node.right, depth + 1, max_depth)

    # 随机选择复杂化策略 - 专注于对数变换
    strategies = [
        _apply_log_addition_rule,
        _apply_log_subtraction_rule,
        _apply_power_rule,
        _apply_change_of_base,
        _split_numeric_coefficient,
        _introduce_identity_operations,
        _apply_log_multiplication_rule,
        _apply_exponent_log_relation,
        _introduce_fraction_forms,
        _apply_double_change_of_base,
        _introduce_nested_logarithms,
        _apply_reciprocal_rule,
        _replace_constant_with_logarithm,  # 新增：将常数替换为对数
        _introduce_polynomial_log_forms,   # 新增：引入多项式对数形式
        _combine_multiple_rules
    ]

    # 根据深度调整策略权重
    if depth < max_depth // 2:
        strategy = choice(strategies)
    else:
        # 后半段更倾向于复杂变换
        strategy = choice(strategies)

    return strategy(node, depth, max_depth)


def _replace_constant_with_logarithm(node: expr.Node, depth: int, max_depth: int) -> expr.Node:
    """将常数替换为对数表达式"""
    if isinstance(node, expr.Value) and isinstance(node.value, (int, float)):
        value = node.value

        # 常见对数值替换
        if value == 1:
            replacements = [
                expr.Log(expr.Value(2), expr.Value(2)),
                expr.Log(expr.Value(3), expr.Value(3)),
                expr.Log(expr.Value(5), expr.Value(5)),
                expr.Log(expr.Value(10), expr.Value(10)),
                expr.Add(
                    expr.Log(expr.Value(2), expr.Value(5)),
                    expr.Log(expr.Value(5), expr.Value(2))
                ),  # lg5 + lg2 = lg10 = 1
            ]
            return choice(replacements)

        elif value == 2:
            replacements = [
                expr.Log(expr.Value(2), expr.Value(4)),
                expr.Log(expr.Value(3), expr.Value(9)),
                expr.Log(expr.Value(5), expr.Value(25)),
                expr.Mul(expr.Value(2), expr.Log(
                    expr.Value(2), expr.Value(2))),
                expr.Add(
                    expr.Log(expr.Value(2), expr.Value(2)),
                    expr.Log(expr.Value(2), expr.Value(2))
                ),
            ]
            return choice(replacements)

        elif value == 0:
            replacements = [
                expr.Log(expr.Value(2), expr.Value(1)),
                expr.Sub(
                    expr.Log(expr.Value(2), expr.Value(4)),
                    expr.Log(expr.Value(2), expr.Value(4))
                ),
            ]
            return choice(replacements)

        elif value > 0 and random() < 0.3:
            # 尝试将其他正数表示为对数形式
            base = choice([2, 3, 5, 10])
            if value == base:
                return expr.Log(expr.Value(base), expr.Value(base))
            elif value == base**2:
                return expr.Log(expr.Value(base), expr.Value(base**2))
            elif value == base**3:
                return expr.Log(expr.Value(base), expr.Value(base**3))

    return node


def _introduce_polynomial_log_forms(node: expr.Node, depth: int, max_depth: int) -> expr.Node:
    """引入多项式对数形式，如 (lg2)^2 + lg2*lg5 + lg5"""
    if isinstance(node, expr.Value) and isinstance(node.value, (int, float)) and node.value > 0:
        if random() < 0.2:
            # 创建多项式对数表达式
            forms = [
                # lg2lg5 + lg2lg2 + lg5 类型
                lambda: expr.Add(
                    expr.Add(
                        expr.Mul(
                            expr.Log(expr.Value(10), expr.Value(2)),
                            expr.Log(expr.Value(10), expr.Value(5))
                        ),
                        expr.Pow(
                            expr.Log(expr.Value(10), expr.Value(2)),
                            expr.Value(2)
                        )
                    ),
                    expr.Log(expr.Value(10), expr.Value(5)),
                ),
                # lg2lg5 + lg5lg5 + lg2
                lambda: expr.Add(
                    expr.Add(
                        expr.Mul(
                            expr.Log(expr.Value(10), expr.Value(2)),
                            expr.Log(expr.Value(10), expr.Value(5))
                        ),
                        expr.Pow(
                            expr.Log(expr.Value(10), expr.Value(5)),
                            expr.Value(2)
                        )
                    ),
                    expr.Log(expr.Value(10), expr.Value(2)),
                ),
                # (lg2)^2 + (lg5)^2 + 2(lg2)(lg5) 类型
                lambda: expr.Add(
                    expr.Add(
                        expr.Mul(
                            expr.Log(expr.Value(10), expr.Value(2)),
                            expr.Log(expr.Value(10), expr.Value(2))
                        ),
                        expr.Mul(
                            expr.Log(expr.Value(10), expr.Value(5)),
                            expr.Log(expr.Value(10), expr.Value(5))
                        )
                    ),
                    expr.Mul(
                        expr.Mul(
                            expr.Value(2),
                            expr.Log(expr.Value(10), expr.Value(5))
                        ),
                        expr.Log(expr.Value(10), expr.Value(2))
                    )
                )
            ]
            return expr.Mul(node, choice(forms)())

    elif isinstance(node, expr.Add) and random() < 0.1:
        # 在加法表达式中引入对数多项式
        return expr.Mul(
            expr.Add(
                expr.Log(expr.Value(10), expr.Value(2)),
                expr.Log(expr.Value(10), expr.Value(5))
            ),
            node
        )

    return node


def _apply_log_addition_rule(node: expr.Node, depth: int, max_depth: int) -> expr.Node:
    """应用对数加法法则：log_a(b) = log_a(b*c) - log_a(c)"""
    if isinstance(node, expr.Log):
        base = node.left
        arg = node.right

        # 更多样的乘数选择
        multiplier_choices = [
            # 底数的幂次
            lambda: expr.Pow(base, expr.Value(randint(1, 4))),
            # 简单数字
            lambda: expr.Value(choice([2, 3, 4, 5, 6, 8, 9])),
            # 分数形式
            lambda: expr.Div(expr.Value(1), expr.Value(choice([2, 3, 4]))),
            # 另一个对数表达式
            lambda: expr.Log(
                expr.Value(choice([2, 3, 5])),
                expr.Value(choice([4, 8, 9, 16]))
            ),
            # 加法表达式
            lambda: expr.Add(
                expr.Value(randint(1, 3)),
                expr.Value(randint(1, 3))
            )
        ]

        multiplier = choice(multiplier_choices)()
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

        divisor_choices = [
            lambda: expr.Pow(base, expr.Value(randint(1, 3))),
            lambda: expr.Value(choice([2, 3, 4, 5, 6])),
            lambda: expr.Mul(
                expr.Value(choice([2, 3])),
                expr.Value(choice([2, 3]))
            ),
            lambda: expr.Log(
                expr.Value(choice([2, 3])),
                expr.Value(choice([4, 8, 9]))
            )
        ]

        divisor = choice(divisor_choices)()
        new_arg = expr.Div(arg, divisor)
        log1 = expr.Log(base, new_arg)
        log2 = expr.Log(base, divisor)

        return expr.Add(log1, log2)
    return node


def _apply_log_multiplication_rule(node: expr.Node, depth: int, max_depth: int) -> expr.Node:
    """应用对数乘法法则：k * log_a(b) = log_a(b^k)"""
    if isinstance(node, expr.Mul) and isinstance(node.left, expr.Value) and isinstance(node.right, expr.Log):
        k = node.left.value
        log_expr = node.right

        if isinstance(k, (int, float)) and k > 0:
            new_arg = expr.Pow(log_expr.right, expr.Value(k))
            return expr.Log(log_expr.left, new_arg)

    return node


def _apply_power_rule(node: expr.Node, depth: int, max_depth: int) -> expr.Node:
    """应用幂法则增强版"""
    if isinstance(node, expr.Log):
        k = randint(2, 5)
        base = node.left
        arg = node.right

        # 更多样的幂次处理
        if random() < 0.4:
            # 使用分数幂次
            new_arg = expr.Pow(arg, expr.Div(expr.Value(1), expr.Value(k)))
            inner_log = expr.Log(base, new_arg)
            return expr.Mul(expr.Value(k), inner_log)
        else:
            # 使用整数幂次
            new_arg = expr.Pow(arg, expr.Value(k))
            inner_log = expr.Log(base, new_arg)
            return expr.Mul(expr.Div(expr.Value(1), expr.Value(k)), inner_log)
    return node


def _apply_change_of_base(node: expr.Node, depth: int, max_depth: int) -> expr.Node:
    """应用换底公式增强版"""
    if isinstance(node, expr.Log):
        old_base = node.left
        arg = node.right

        # 更多样的新底数选择
        new_base_choices = [
            expr.Value(2), expr.Value(3), expr.Value(5), expr.Value(10),
            expr.Value('e'), expr.Value(6), expr.Value(7),
            expr.Pow(expr.Value(2), expr.Value(2)),
            expr.Pow(expr.Value(3), expr.Value(2)),
            expr.Pow(expr.Value(2), expr.Value(3)),
            expr.Add(expr.Value(1), expr.Value(1)),  # 1+1=2
            expr.Mul(expr.Value(2), expr.Value(2)),  # 2*2=4
        ]

        new_base = choice(new_base_choices)
        numerator = expr.Log(new_base, arg)
        denominator = expr.Log(new_base, old_base)

        return expr.Div(numerator, denominator)
    return node


def _apply_double_change_of_base(node: expr.Node, depth: int, max_depth: int) -> expr.Node:
    """双重换底：先换到一个中间底数，再换到另一个底数"""
    if isinstance(node, expr.Log):
        # 第一次换底
        intermediate_base = expr.Value(choice([2, 3, 5, 10]))
        first_change = expr.Div(
            expr.Log(intermediate_base, node.right),
            expr.Log(intermediate_base, node.left)
        )

        # 对结果再次应用复杂化
        return make_chaos(first_change, depth + 1, max_depth)
    return node


def _apply_exponent_log_relation(node: expr.Node, depth: int, max_depth: int) -> expr.Node:
    """利用指数和对数的关系：a^{log_a(b)} = b"""
    if isinstance(node, expr.Value) and isinstance(node.value, (int, float)) and node.value > 0:
        base = expr.Value(choice([2, 3, 5, 10, 'e']))
        return expr.Pow(base, expr.Log(base, expr.Value(node.value)))
    return node


def _introduce_nested_logarithms(node: expr.Node, depth: int, max_depth: int) -> expr.Node:
    """引入嵌套对数"""
    if isinstance(node, expr.Log):
        if random() < 0.2:
            # 在对数内部再嵌套一个对数
            base = expr.Value(choice([2, 3, 5]))
            nested_log = expr.Log(
                base,
                expr.Pow(base, node.right)
            )
            return expr.Log(node.left, nested_log)
    return node


def _introduce_fraction_forms(node: expr.Node, depth: int, max_depth: int) -> expr.Node:
    """引入分数形式"""
    if isinstance(node, expr.Value) and isinstance(node.value, (int, float)):
        if node.value > 1 and random() < 0.4:
            # 将整数表示为分数形式
            numerator = node.value * randint(2, 4)
            denominator = randint(2, 4)
            return expr.Div(expr.Value(numerator), expr.Value(denominator))

    elif isinstance(node, (expr.Add, expr.Sub)):
        # 将加减法转换为同分母分数加减
        if random() < 0.3:
            denominator = expr.Value(randint(2, 5))
            left_num = expr.Mul(node.left, denominator)
            right_num = expr.Mul(node.right, denominator)

            if isinstance(node, expr.Add):
                numerator = expr.Add(left_num, right_num)
            else:
                numerator = expr.Sub(left_num, right_num)

            return expr.Div(numerator, denominator)

    return node


def _apply_reciprocal_rule(node: expr.Node, depth: int, max_depth: int) -> expr.Node:
    """应用倒数规则：log_a(b) = 1 / log_b(a)"""
    if isinstance(node, expr.Log):
        return expr.Div(
            expr.Value(1),
            expr.Log(node.right, node.left)
        )
    return node


def _combine_multiple_rules(node: expr.Node, depth: int, max_depth: int) -> expr.Node:
    """组合多种规则"""
    if isinstance(node, expr.Log) and random() < 0.7:
        # 先应用换底公式
        temp = _apply_change_of_base(node, depth, max_depth)
        # 再对结果应用幂法则
        return _apply_power_rule(temp, depth, max_depth)
    return node


def _split_numeric_coefficient(node: expr.Node, depth: int, max_depth: int) -> expr.Node:
    """拆分数值系数增强版"""
    if isinstance(node, expr.Value) and isinstance(node.value, (int, float)) and abs(node.value) > 1:
        if random() < 0.6:
            # 加法拆分
            if node.value > 1:
                m = randint(1, int(node.value) - 1)
                n = node.value - m
                return expr.Add(expr.Value(m), expr.Value(n))
            else:
                m = randint(int(node.value) + 1, 0)
                n = node.value - m
                return expr.Add(expr.Value(m), expr.Value(n))
        else:
            # 乘法拆分
            if isinstance(node.value, int) and node.value > 1:
                factors = [i for i in range(
                    2, abs(node.value)) if node.value % i == 0]
                if factors:
                    m = choice(factors)
                    n = node.value // m
                    return expr.Mul(expr.Value(m), expr.Value(n))
            # 分数拆分
            if random() < 0.4:
                return expr.Div(
                    expr.Value(node.value * randint(2, 4)),
                    expr.Value(randint(2, 4))
                )
    return node


def _introduce_identity_operations(node: expr.Node, depth: int, max_depth: int) -> expr.Node:
    """引入恒等运算增强版"""
    # 更多样的恒等形式
    one_forms: List[expr.Node] = [
        expr.Value(1),
        expr.Div(expr.Value(2), expr.Value(2)),
        expr.Div(expr.Value(3), expr.Value(3)),
        expr.Pow(expr.Value(1), expr.Value(randint(2, 5))),
        expr.Log(expr.Value(2), expr.Value(2)),
        expr.Log(expr.Value(3), expr.Value(3)),
        expr.Add(expr.Value(1), expr.Value(0)),
        expr.Sub(expr.Value(2), expr.Value(1)),
    ]

    zero_forms: List[expr.Node] = [
        expr.Value(0),
        expr.Sub(expr.Value(2), expr.Value(2)),
        expr.Sub(expr.Value(3), expr.Value(3)),
        expr.Mul(expr.Value(0), expr.Value(randint(2, 5))),
        expr.Div(expr.Value(0), expr.Value(randint(1, 5))),
    ]

    if random() < 0.5:
        if isinstance(node, expr.Mul):
            return expr.Mul(node, choice(one_forms))
        elif isinstance(node, expr.Add):
            return expr.Add(node, choice(zero_forms))
        elif isinstance(node, expr.Div):
            # 分子分母同乘一个非零表达式
            multiplier = choice(
                [f for f in one_forms if not isinstance(f, expr.Value) or f.value != 0])
            return expr.Div(
                expr.Mul(node.left, multiplier),
                expr.Mul(node.right, multiplier)
            )

    return node


# 新增：批量生成复杂对数表达式
def generate_complex_logarithm_exercises(count: int = 10, max_depth: int = 4) -> List[tuple]:
    """
    生成复杂对数表达式练习题
    返回: [(复杂表达式, 简化表达式), ...]
    """
    exercises = []

    # 基础对数表达式模板
    base_templates = [
        # 简单对数
        lambda: expr.Log(expr.Value(2), expr.Value(8)),
        lambda: expr.Log(expr.Value(3), expr.Value(27)),
        lambda: expr.Log(expr.Value(5), expr.Value(25)),
        lambda: expr.Log(expr.Value(10), expr.Value(100)),

        # 带系数的对数
        lambda: expr.Mul(expr.Value(2), expr.Log(
            expr.Value(2), expr.Value(4))),
        lambda: expr.Mul(expr.Value(3), expr.Log(
            expr.Value(3), expr.Value(9))),

        # 对数运算
        lambda: expr.Add(
            expr.Log(expr.Value(2), expr.Value(8)),
            expr.Log(expr.Value(2), expr.Value(4))
        ),
        lambda: expr.Sub(
            expr.Log(expr.Value(2), expr.Value(16)),
            expr.Log(expr.Value(2), expr.Value(4))
        ),

        # 多项式对数形式
        lambda: expr.Value(1),  # 会被替换为复杂形式
        lambda: expr.Value(2),  # 会被替换为复杂形式
    ]

    for _ in range(count):
        # 选择基础模板
        base_expr = choice(base_templates)()

        # 应用复杂化
        complex_expr = make_chaos(base_expr, max_depth=max_depth)

        exercises.append((complex_expr, base_expr))

    return exercises


# 使用示例
if __name__ == "__main__":
    # 生成10个复杂对数表达式练习题
    exercises = generate_complex_logarithm_exercises(10, max_depth=4)

    for i, (complex_expr, simple_expr) in enumerate(exercises, 1):
        print(f"题目 {i}:")
        print(f"复杂表达式: {complex_expr}")
        print(f"简化目标: {simple_expr}")
        print("---")
