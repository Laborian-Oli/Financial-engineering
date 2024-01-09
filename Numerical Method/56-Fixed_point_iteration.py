"""
 Author: 2020200229
 Creation time: 2022/10/11
 Filename: 56-Fixed_point_iteration
 """
# 二分法、不动点迭代算法、不动点迭代加速算法、牛顿法、割线法
# 使用符号运算，只需要函数表达式，程序自动进行求导等操作，泛用性好，运算较慢
import sympy.stats  # 使用符号计算
import time


def bisection_method(aimfunc, left, right, dep=15, acc=10):  # 二分法迭代
    iter_list = []  # 局部变量
    m = 0
    if aimfunc(left)[0] * aimfunc(right)[0] >= 0:
        return '初始点异常'
    while abs(right - left) > 10**(- acc - 1):
        midpoint = (left + right) / 2
        iter_list.append(midpoint)
        if m == dep:
            break
        else:
            if aimfunc(midpoint)[0] * aimfunc(left)[0] < 0:
                right = midpoint
                m += 1
            elif aimfunc(midpoint)[0] * aimfunc(left)[0] > 0:
                left = midpoint
                m += 1
            else:
                break
    for _ in range(m):
        print(f'第{_ + 1:>4}次迭代结果为：{iter_list[_]}')
    return midpoint, iter_list


def fixed_point_method(aimfunc, the_p, dep=20, acc=5):  # 不动点迭代，f(x) = x
    m = -1
    iter_list = [the_p]
    while abs(aimfunc(the_p)[0] - the_p) > 10**(- acc - 1):
        if m == dep:
            break
        else:
            the_p = aimfunc(the_p)[0]
            iter_list.append(the_p)
            m += 1
    for _ in range(m+1):
        print(f'第{_:>4}次迭代结果为：{iter_list[_]}')
    return the_p, iter_list


def fixed_point_method_acceleration(aimfunc, the_p, dep=20, acc=5):  # 不动点迭代，加速算法
    m = 0
    iter_list = [the_p]
    der = sympy.diff(aimfunc()[1], 'x')
    while abs(aimfunc(the_p)[0] - the_p) > 10 ** (- acc - 1):  # 这个判断标准应该需要修改
        if m == dep:
            break
        else:
            lam = - der.evalf(subs={'x': the_p})
            the_p = (lam / (lam + 1)) * the_p + aimfunc(the_p)[0] / (lam + 1)
            iter_list.append(the_p)
            m += 1
    for _ in range(m+1):
        print(f'第{_:>4}次迭代结果为：{iter_list[_]}')
    return the_p, iter_list


def Newton_method(aimfunc, the_p, dep=5):  # 牛顿法，求零点
    m = 0
    iter_list = [the_p]
    der = sympy.diff(aimfunc()[1], 'x')  # 这里的自变量需要按照需要调整(否则。。。)，懒得优化
    while True:
        if m == dep:
            break
        else:
            the_p = the_p - aimfunc(the_p)[0]/der.evalf(subs={'x': the_p})
            iter_list.append(the_p)
            m += 1
    for _ in range(m + 1):
        print(f'第{_:>4}次迭代结果为：{iter_list[_]}')
    return the_p, iter_list


def secant_method(aimfunc, p_0, p_1, dep=10):
    m = 0
    iter_list = []
    while True:
        if m == dep:
            break
        else:
            p_trans = p_1
            p_1 = p_1 - aimfunc(p_1)[0] / ((aimfunc(p_1)[0] - aimfunc(p_0)[0]) / (p_1 - p_0))
            p_0 = p_trans
            iter_list.append(p_1)
            m += 1
    for _ in range(m):
        print(f'第{_ + 1:>4}次迭代结果为：{iter_list[_]}')
    return p_1, iter_list


# 为方便求导，目标函数同时返回函数表达式
def func_a(p=1):  # e^x = 2 的解
    x = sympy.symbols('x')
    f = sympy.exp(x) - 2
    return f.evalf(subs={x: p}), f


def func_b(p=0):  # 求根号2
    x = sympy.symbols('x')
    f = x*x - 2
    return f.evalf(subs={x: p}), f


def func_c(p=0):  # cosx，测试不动点迭代
    x = sympy.symbols('x')
    f = sympy.cos(x)
    return f.evalf(subs={x: p}), f


def func_d(p=0):  # cosx-x，测试牛顿法，割线法
    x = sympy.symbols('x')
    f = sympy.cos(x) - x
    return f.evalf(subs={x: p}), f


print(Newton_method(func_c, 10))
print(f'运行时长：{time.process_time()}')
