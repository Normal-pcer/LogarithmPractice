from random import choice, randint
from chaos import make_chaos
# from copy import deepcopy
import expr

def gen_ans() -> tuple[expr.Node, int]:
    # 生成一个友好的单项式答案
    base = choice([2, 3, 4, 5, 10, 'e'])
    exp = randint(1, 4)
    
    if isinstance(base, str):
        if exp != 1:
            arg_node = expr.Pow(expr.Value(base), expr.Value(exp))
        else:
            arg_node = expr.Value(base)
    else:
        arg_node = expr.Value(base ** exp)
    
    return (expr.Log(expr.Value(base), arg_node), exp)

def main() -> None:
    lis = [gen_ans() for _ in range(500)]
    lis = [f"$$ {make_chaos(make_chaos(expr))} = {ans} $$" for expr, ans in lis]
    lis.sort(key = len)
    print("\n".join(lis[400:]))

if __name__ == '__main__':
    main()
