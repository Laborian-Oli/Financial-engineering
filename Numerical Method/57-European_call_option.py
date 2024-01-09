"""
 Author: 2020200229
 Creation time: 2022/10/24
 Filename: 57-European_call_option
 """
# 这里没有使用符号运算而使用数值运算，以加快运算速度
import scipy.stats
import math
import time


def bisection_method(aimfunc, left, right, dep=100, acc=15):
    iter_list = []  # 局部变量
    m = 0
    if aimfunc(left) * aimfunc(right) >= 0:
        return '初始点异常'
    while abs(right - left) > 10**(- acc - 1):
        midpoint = (left + right) / 2
        iter_list.append(midpoint)
        if m == dep:
            break
        else:
            if aimfunc(midpoint) * aimfunc(left) < 0:
                right = midpoint
                m += 1
            elif aimfunc(midpoint) * aimfunc(left) > 0:
                left = midpoint
                m += 1
            else:
                break
    for _ in range(m):
        print(f'第{_ + 1:>4}次迭代结果为：{iter_list[_]}')
    return midpoint, iter_list


def Newton_method(aimfunc, aimfunc_diff, the_p, dep=11):
    m = 0
    iter_list = [the_p]
    while True:
        if m == dep:
            break
        else:
            the_p = the_p - aimfunc(the_p)/aimfunc_diff(the_p)
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
            p_1 = p_1 - aimfunc(p_1) / ((aimfunc(p_1) - aimfunc(p_0)) / (p_1 - p_0))
            p_0 = p_trans
            iter_list.append(p_1)
            m += 1
    for _ in range(m):
        print(f'第{_ + 1:>4}次迭代结果为：{iter_list[_]}')
    return p_1, iter_list


# stats.norm.cdf(α,均值,方差)：累积概率密度函数
def B_S(sig, S=100, K=105, r=0.05, T=0.25, zero_point=3.05):
    d_1 = (math.log(S / K) + (r + sig**2 / 2) * T) / (sig * T ** 0.5)
    d_2 = (math.log(S / K) + (r - sig**2 / 2) * T) / (sig * T ** 0.5)
    C = S * scipy.stats.norm.cdf(d_1, 0, 1) - K * math.exp(-r * T) * scipy.stats.norm.cdf(d_2, 0, 1)
    f = C - zero_point
    return f


# stats.norm.pdf(α,均值,方差)：概率密度函数
def B_S_diff(sig, S=100, K=105, r=0.05, T=0.25):
    d_1 = (math.log(S / K) + (r + sig ** 2 / 2) * T) / (sig * T ** 0.5)
    d_2 = (math.log(S / K) + (r - sig ** 2 / 2) * T) / (sig * T ** 0.5)
    d_1_diff = - math.log(S / K) / (sig ** 2 * T ** 0.5) - (r * T ** 0.5) / sig ** 2 + (T ** 0.5) / 2
    d_2_diff = - math.log(S / K) / (sig ** 2 * T ** 0.5) - (r * T ** 0.5) / sig ** 2 - (T ** 0.5) / 2
    f = S * d_1_diff * scipy.stats.norm.pdf(d_1, 0, 1) \
        - K * math.exp(-r * T) * d_2_diff * scipy.stats.norm.pdf(d_2, 0, 1)
    return f


print(bisection_method(B_S, 0.1, 1))
# print(Newton_method(B_S, B_S_diff, 1))
# print(secant_method(B_S, 0.1, 1))
print(f'运行时长：{time.process_time()}')