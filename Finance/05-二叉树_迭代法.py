"""
 Author: 2020200229
 Creation time: 2023/5/9
 Filename: 05_二叉树_迭代法
 """
import math
from matplotlib import pyplot as plt


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

    def v(self, n=0, s=None):
        """计算时刻n的期权价格，默认为计算时刻0"""
        if s is None:
            s = self.s_0
        return max(s - self.k, 0) if n == self.step_num else ((self.p * self.v(n+1, s * self.u) +
                                                               (self.q * self.v(n+1, s * self.d))) / self.et)


if __name__ == '__main__':
    option = Option(s_0=50, k=52, r=0.05, t=2, sigma=math.log(1.2), step_num=4)
    print(option.v())

    # plt.style.use('default')  # 套用Style
    # plt.rcParams['font.sans-serif'] = ['SimHei']  # 正常显示中文标签
    # plt.rcParams['axes.unicode_minus'] = False  # 用来正常显示负号
    # plt.figure(figsize=(8, 6))  # 画布大小
    #
    # step = 20
    # y = []
    # x = []
    # for _ in range(21):
    #     option = Option(s_0=50, k=52, r=0.05, t=2, sigma=math.log(1.2), step_num=_ + 1)
    #     x.append(_ + 1)
    #     y.append(option.v())
    #
    #
    # plt.plot(x, y, marker='o', alpha=0.8)
    #
    # plt.grid(visible=True, which='major', axis='both', linestyle='-.')  # 网格线
    #
    # plt.title('基本初等函数的函数图像', loc='center')
    # plt.xlabel('X轴', loc='right')
    # plt.ylabel('Y轴', loc='top')
    #
    # plt.show()
