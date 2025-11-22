from random import choice, randint
from chaos import make_chaos
import expr

def gen_ans() -> expr.Node:
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
    
    return expr.Log(expr.Value(base), arg_node)

def main() -> None:
    for _ in range(100):
        ans = gen_ans()
        chaos = make_chaos(ans)
        print('$$', ans, '=', chaos, '$$')

if __name__ == '__main__':
    main()
