from matplotlib import pyplot as plt
import numpy as np


class Credit:
    def __init__(self, p, credit_exposure, loss_given_default):
        self.p = p
        self.ce = credit_exposure
        self.lgd = loss_given_default

    def get_b(self):
        p = np.random.rand()
        if p > self.p:
            return 0
        elif p <= self.p:
            return 1

    def get_ce(self):
        return np.random.randn() + self.ce

    def get_lgd(self):
        return np.random.randn() + self.lgd


def cl_mean(p, credit_exposure, loss_given_default):
    a = Credit(p, credit_exposure, loss_given_default)
    cl_ls = []
    for _ in range(10000):
        cl = a.get_b() * a.get_ce() * a.get_lgd()
        cl_ls.append(cl)
    cl_array = np.array(cl_ls)
    mean = cl_array.mean()
    sd = cl_array.std()
    return mean, sd


def main():
    if __name__ == '__main__':
        n = 100
        mean_ls = []
        sd_ls = []
        p_ls = []
        for _ in range(n):
            p = (10 ** (5 * _/100 - 3)) / (10 ** (5 * 99/100 - 3) * 10)
            mean, sd = cl_mean(p, 10, 0.4)
            p_ls.append(p)
            mean_ls.append(mean)
            sd_ls.append(sd)

        plt.style.use('default')  # 套用Style
        plt.rcParams['font.sans-serif'] = ['SimHei']  # 正常显示中文标签
        plt.rcParams['axes.unicode_minus'] = False  # 用来正常显示负号
        plt.figure(figsize=(8, 6))  # 画布大小

        plt.plot(p_ls, mean_ls, marker='o', c='lightgreen', alpha=1, label='均值')
        plt.plot(p_ls, sd_ls, marker='o', c='orange', alpha=1, label='标准差')

        plt.legend(loc='best')
        # plt.title('资产组合有效边界(Portfolio Efficient Frontier)', loc='center')
        # plt.ylabel('收益率（%）', loc='top')
        # plt.xlabel('标准差（%）', loc='right')
        plt.grid(visible=True, which='major', axis='both', linestyle='-.')  # 网格线

        plt.show()
        plt.close()


main()
