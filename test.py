from expr import *

def create_complex_expression():
    """创建一个包含对数外套乘方操作的复杂表达式"""
    
    # 基础数值
    x = Value(2)
    y = Value(3)
    e = Value("e")
    pi = Value("pi")
    
    # 创建各种对数表达式
    log_10 = Log(Value(10), x)  # log₁₀(2)
    ln_e = Log(e, Value(5))     # ln(5)
    log_custom = Log(y, x)      # log₃(2)
    
    # 对数外套乘方
    pow_log1 = Pow(log_10, Value(2))        # (log₁₀(2))²
    pow_log2 = Pow(ln_e, Value(3))          # (ln(5))³
    pow_log3 = Pow(log_custom, Value(4))    # (log₃(2))⁴
    
    # 更复杂的嵌套
    complex_log2 = Log(Mul(x, y), Add(x, y))                   # log₆(5)
    pow_complex_log = Pow(complex_log2, Value(2))              # (log₆(5))²
    
    # 多层嵌套的对数乘方
    very_complex = Pow(
        Log(
            Add(x, y),  # base: 2+3=5
            Pow(
                Log(e, Mul(pi, x)),  # arg: ln(π×2)
                Value(2)
            )
        ),
        Value(3)
    )  # (log₅((ln(2π))²))³
    
    # 构建最终的大表达式
    expr = Add(
        Sub(
            Mul(pow_log1, pow_log2),
            Div(pow_log3, pow_complex_log)
        ),
        very_complex
    )
    
    return expr

# 测试表达式
if __name__ == "__main__":
    expr = create_complex_expression()
    
    print("LaTeX 表达式:")
    print(expr)
    print("\n" + "="*50 + "\n")
    
    print("计算结果:")
    try:
        result = expr.calc()
        print(f"结果: {result}")
        print(f"科学计数法: {result:.10e}")
    except Exception as e:
        print(f"计算错误: {e}")
    
    print("\n" + "="*50 + "\n")
    
    # 单独测试对数外套乘方的部分
    print("测试对数外套乘方部分:")
    
    # 测试 log₁₀(2)²
    log10_2 = Log(Value(10), Value(2))
    pow_log10_2 = Pow(log10_2, Value(2))
    print(f"log10(2)² = {pow_log10_2}")
    print(f"计算结果: {pow_log10_2.calc()}")
    
    print()
    
    # 测试 ln(5)³  
    ln_5 = Log(Value("e"), Value(5))
    pow_ln_5 = Pow(ln_5, Value(3))
    print(f"ln(5)³ = {pow_ln_5}")
    print(f"计算结果: {pow_ln_5.calc()}")
    
    print()
    
    # 测试 log₃(2)⁴
    log3_2 = Log(Value(3), Value(2))
    pow_log3_2 = Pow(log3_2, Value(4))
    print(f"log3(2)⁴ = {pow_log3_2}")
    print(f"计算结果: {pow_log3_2.calc()}")