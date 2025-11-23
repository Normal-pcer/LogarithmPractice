from random import choice, randint
from chaos import make_chaos
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
    print(r"""\documentclass[12pt]{article}
\usepackage[a4paper, margin=1in]{geometry}
\usepackage{amsmath}
\usepackage{ctex}

\title{对数运算测试题}
\date{}

\begin{document}

\maketitle

\begin{enumerate}""")

    n = 800
    lis = [gen_ans() for _ in range(n)]
    lis = [(f"\\item $ {make_chaos(make_chaos(expr))} = \\underline{{\\hspace{{2cm}}}} $", ans) for expr, ans in lis]
    lis.sort(key = lambda x: len(x[0]))

    for item, _ in lis[(n - 150): (n - 50)]:
        print(item)
    
    print("参考答案\n")

    for i in range(n - 150, n - 50):
        print(lis[i][1], end = ("; " if (i + 1) % 10 else "\n\n"))

    print(r"""
\end{enumerate}

\end{document}""")

if __name__ == '__main__':
    main()
