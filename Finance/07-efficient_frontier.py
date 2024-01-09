import pandas
import numpy as np
from matplotlib import pyplot as plt
import cvxopt as opt
from cvxopt import blas, solvers


solvers.options['show_progress'] = False  # 不显示计算过程


def optimal_portfolio(average_return, cov):
    """
    运用非线性规划求有效边界，依赖cvxopt库中的solvers.qp()

    - average_return: 平均收益的向量
    - cov: 协方差矩阵，可以为array
    """
    # 生成拉格朗日乘子的序列
    n = len(average_return)
    steps = 100
    mus = [10 ** (5 * t/steps - 3) for t in range(steps)]

    # opt.qp()要求参数全部是opt.matrix
    cov_mat = opt.matrix(cov)
    q = opt.matrix(average_return)

    # 限制矩阵
    G = - opt.matrix(np.eye(n))
    h = opt.matrix(0.0, (n, 1))
    A = opt.matrix(1.0, (1, n))
    b = opt.matrix(1.0)

    # solvers.qp()每次返回一个dict，包含'x'、'y'等键值对，值为一个matrix，这里只需要'x'，存入list
    portfolios = [solvers.qp(mu * cov_mat, - q, G, h, A, b)['x'] for mu in mus]

    # 计算收益率和标准差，blas.dot()即转置相乘
    returns = [blas.dot(q, _) for _ in portfolios]
    sd = [np.sqrt(blas.dot(_, cov_mat * _)) for _ in portfolios]
    return returns, sd


def get_points(num, average_return, cov):
    """
    用随机生成的投资组合来描绘有效边界

    - num: 生成多少次
    - average_return: 平均收益的向量
    - cov: 协方差矩阵，可以为array
    使用了迪利克雷分布
    出于一致性，使用了cvxopt
    标准差大于8的就不画了
    """
    x_ls = []
    y_ls = []
    average_return = opt.matrix(average_return)
    cov = opt.matrix(cov)
    for _ in range(num):
        w_ls = opt.matrix(np.random.dirichlet(np.ones(8)))
        x = np.sqrt(blas.dot(w_ls, cov * w_ls))
        if x <= 8:
            y_ls.append(blas.dot(w_ls, average_return))
            x_ls.append(x)
    return y_ls, x_ls


def main():
    if __name__ == '__main__':
        # 导入和整理数据
        raw_data = pandas.read_excel('MPT-Efficient-Frontier-and-CAL_data.xlsx')
        data = raw_data.drop(index=0, columns='日期')
        # 生成协方差矩阵
        data = data.astype(float)
        cov_array = np.array(data.cov())  # .cov函数只操作类型是数的元素
        av_return_col = np.array(data.mean()).reshape([-1, 1])

        yields, risks = optimal_portfolio(average_return=av_return_col, cov=cov_array)
        yields_rand, risks_rand = get_points(num=100000, average_return=av_return_col, cov=cov_array)

        # 画图
        plt.style.use('default')  # 套用Style
        plt.rcParams['font.sans-serif'] = ['SimHei']  # 正常显示中文标签
        plt.rcParams['axes.unicode_minus'] = False  # 用来正常显示负号
        plt.figure(figsize=(8, 6))  # 画布大小

        plt.scatter(risks_rand, yields_rand, marker='o', c='lightgreen', alpha=0.5, label='随机资产组合')
        plt.plot(risks, yields, marker='P', c='orange', alpha=0.5, label='有效边界')

        plt.legend(loc='best')
        plt.title('资产组合有效边界(Portfolio Efficient Frontier)', loc='center')
        plt.ylabel('收益率（%）', loc='top')
        plt.xlabel('标准差（%）', loc='right')
        plt.grid(visible=True, which='major', axis='both', linestyle='-.')  # 网格线

        plt.show()
        plt.close()


main()
