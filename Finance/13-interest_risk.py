"""
 Author: 2020200229
 Creation time: 2023/8/19
 Filename: 13-interest_risk
 """
import numpy as np
from matplotlib import pyplot as plt
import pandas


def cash_flow(principal, current_yield, year):
    """
    生成一个现金流的array
    """
    cf = np.empty(year, dtype=float)
    coupon = current_yield * principal
    for _ in range(year):
        cf[_] = coupon
    cf[-1] += principal
    return cf


def discount(c_f, dr):
    """
    对现金流贴现
    """
    pv_gross = 0
    duration = 0
    for _ in range(len(c_f)):
        pv = c_f[_] / ((dr + 1) ** (_ + 1))
        duration += pv * (_ + 1)
        pv_gross += pv
    if (pv_gross - 0)**2 < 0.00001:
        duration = None
    else:
        duration = duration / pv_gross
    return pv_gross, duration


def npv_change(c_f, steps=101, min_dr=0, max_dr=1):
    """
    返回NPV随着贴现率变化的Series
    """
    dr_array = np.linspace(min_dr, max_dr, steps)
    npv_array = np.empty(steps, dtype=float)
    duration_array = np.empty(steps, dtype=float)
    for _ in range(steps):
        pv, duration = discount(c_f, dr=dr_array[_])
        npv_array[_] = pv
        duration_array[_] = duration
    index = np.linspace(0, max_dr, steps)
    npv_s = pandas.Series(npv_array, index=index)
    duration_s = pandas.Series(duration_array, index=index)
    return npv_s, duration_s


def plot_it(ser_ls: list, names: list):
    """
    通用画图函数
    """
    plt.style.use('default')  # 套用Style
    plt.rcParams['font.sans-serif'] = ['SimHei']  # 正常显示中文标签
    plt.rcParams['axes.unicode_minus'] = False  # 用来正常显示负号
    plt.figure(figsize=(6, 6))  # 画布大小
    plt.ticklabel_format(style='plain')

    for _ in range(len(ser_ls)):
        plt.plot(ser_ls[_].index, ser_ls[_][:], label=names[_], linewidth=1, linestyle='-', marker='+', markersize=2)
    plt.scatter(0.1, 1000, c='red')  # 画出切点

    plt.legend(loc='best')
    plt.grid(visible=True, which='major', axis='both', linestyle='-.')  # 网格线
    plt.title('N P V', loc='center')
    plt.xlabel('DR', loc='right')
    plt.ylabel('V', loc='top')

    plt.show()


def main():
    if __name__ == '__main__':
        cash_flow_1 = cash_flow(1000, 0.1, 10)
        plot_ls = []
        name_ls = []
        pv_s, d_s = npv_change(cash_flow_1, steps=101, max_dr=2)
        dr = 0.1  # 假设当前折现率为0.1
        y = pv_s[dr]
        print(y)
        d = d_s[dr]
        md = d / (1 + dr)
        k = - md * y
        print(k)
        b = y - k * dr
        duration = pandas.Series((b, 0), index=(0, - b / k))
        plot_ls.append(pv_s)
        plot_ls.append(duration)
        name_ls.append('y_1')
        name_ls.append('基于修正久期的预测')
        plot_it(plot_ls, name_ls)


main()
