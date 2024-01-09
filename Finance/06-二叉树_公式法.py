"""
 Author: 2020200229
 Creation time: 2023/5/9
 Filename: 06-二叉树_公式法
 """
import math


def combination(m, n):
    """计算排列组合"""
    return math.factorial(m) / (math.factorial(n) * (math.factorial(m - n)))


class Option:
    """
    一个普通欧式期权的类，应用于多时段二叉树模型
    """

    def __init__(self, s_0, k, r, t, sigma, step_num):
        """
        - s_0: 标的资产在时刻0的价格
        - k: 期权的执行价格
        - r: 年化利率
        - t: 期权的到期时间，单位为年
        - sigma: 标的资产连续复利收益率的标准差
        - step_num: 二叉树的步数
        """
        self.s_0 = s_0
        self.k = k
        self.r = r
        self.t = t
        self.sigma = sigma
        self.step_num = step_num
        self.et = math.exp(r * (t / step_num))
        self.u = math.exp(sigma * math.sqrt(t / step_num))
        self.d = 1 / self.u
        self.p = (self.et - self.d) / (self.u - self.d)
        self.q = 1 - self.p

    def v_n(self, k):
        """计算到期日期权支付"""
        return max(self.s_0 * (self.u ** k) * (self.d ** (self.step_num - k)) - self.k, 0)

    def c(self):
        """计算期权价格"""
        output = 0
        for _ in range(self.step_num +1):
            output = output + combination(self.step_num, _) * (self.p ** _) * (self.q ** (self.step_num - _)) * self.v_n(_)
        return output / math.exp(self.r * self.t)


option = Option(s_0=50, k=52, r=0.05, t=2, sigma=math.log(1.2), step_num=2)
print(option.c())
