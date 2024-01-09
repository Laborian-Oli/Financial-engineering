"""
 Author: 2020200229
 Creation time: 2023/3/3
 Filename: 69-远期&期权定价
 """
import numpy as np


def option_p(current_p: int or float, strike_p: int or float, r_f, u, d, t, compound_interest=True):
    """
    单步二叉树期权估值模型(期权费)
    - current_p: 标的资产的现值
    - strike_p: 期权的执行价格
    - r_f: 无风险利率
    - u: 可能的收益倍数，较高的分支
    - d: 可能的收益倍数，较低的分支
    - t: 以无风险利率为标准的期数
    - ccompound_interest：是否可以无限复利，默认为可以
    """
    r_0 = np.e ** (r_f * t)  # 无限套利条件下的本息和
    f_u = max((current_p * u) - strike_p, 0)  # 收益函数
    f_d = max((current_p * d) - strike_p, 0)
    if compound_interest is True:
        p = (r_0 - d) / (u - d)  # 风险中性概率
        q = (u - r_0) / (u - d)
        option_premium = (1 / r_0) * ((f_u * p) + (f_d * q))
    elif compound_interest is False:
        p = ((r_f + 1) - d) / (u - d)  # 风险中性概率
        q = (u - (r_f + 1)) / (u - d)
        option_premium = (1 / (r_f + 1)) * ((f_u * p) + (f_d * q))
    else:
        option_premium = None
    return option_premium


def gen_price(current_p: int or float, strike_p: int or float, u: float, d: float, step: int):
    """
    生成每一分叉的价格，放进列表
    - current_p: 标的资产的现值
    - strike_p: 期权的执行价格
    - u: 可能的收益倍数，较高的分支
    - d: 可能的收益倍数，较低的分支
    - step: 二叉树的步数
    """
    p_list = []
    for _ in range(step + 1):
        price = current_p * (u ** (step - _)) * (d ** _)
        income = max(price - strike_p, 0)
        p_list.append(income)
    return p_list


def gen_r_0(r_f, t):
    """
    生成无风险利率下的本息和
    - r_f: 无风险利率
    - t: 以无风险利率为标准的期数
    """
    r_0 = np.e ** (r_f * t)
    return r_0


def gen_p(u, d, r_0):
    """
    计算风险中性利率
    - r_0: 无风险利率下的本息和
    - u: 可能的收益倍数，较高的分支
    - d: 可能的收益倍数，较低的分支
    """
    p = (r_0 - d) / (u - d)
    return p


class IntermediatePrice:
    #  一个价格的类，将每一步二叉树的期权价格放入其中
    def __init__(self, p_list: list, p):
        """
        - p_list: 标的物价格的列表
        - p: 风险中性概率，上涨
        """
        self.p_list = p_list
        self.order = len(p_list)
        self.p = p

    def dimension_reduce(self, r_0):  # 期权价格向上推导折现一次
        if self.order == 1:
            return self
        else:
            new_p_list = []
            for _ in range(self.order - 1):
                new_p = (self.p_list[_] * self.p + self.p_list[_ + 1] * (1 - self.p)) * (1 / r_0)
                new_p_list.append(new_p)
            return IntermediatePrice(p_list=new_p_list, p=self.p)


def final_price(ip: IntermediatePrice, r_0):
    """
    期权价格向上计算至最终价格
    - ip: 一个价格对象
    """
    while ip.order > 1:
        ip = ip.dimension_reduce(r_0)
    return ip


def concordance(current_p, strike_p, r_f, u, d, t, step):
    """
    主要计算过程整合
    """
    price_list = gen_price(current_p=current_p, strike_p=strike_p, u=u, d=d, step=step)
    r_0 = gen_r_0(r_f=r_f, t=t)
    p = gen_p(u=u, d=d, r_0=r_0)
    p_class = IntermediatePrice(p_list=price_list, p=p)
    p_of_op = final_price(ip=p_class, r_0=r_0)
    return p_of_op.p_list[0]


def main():
    if __name__ == '__main__':
        print(concordance(current_p=80, strike_p=80, r_f=0, u=1.125, d=0.875, t=1, step=1))
        # print(option_p(current_p=4, strike_p=5, r_f=0.25, u=2, d=0.5, t=1, compound_interest=False))
        # print(concordance(current_p=4, strike_p=5, r_f=0.25, u=2, d=0.5, t=1, step=1))


main()
