from matplotlib import pyplot as plt
import numpy as np


def simulate_path_vectorize(s_0, mu, sigma, t, n, rep=100):
    """
    使用向量化计算价格变化路径

    - s_0: 期初价格
    - mu: 无风险利率
    - sigma:
    - t: 间隔
    - n: 总期数
    - rep: 模拟次数
    """
    logpaths = np.zeros((rep, n + 1))
    logpaths[:, 0] = np.log(s_0)
    dt = t / n
    nudt = (mu - 0.5 * sigma ** 2) * dt
    sidt = sigma * np.sqrt(dt)
    increments = nudt + sidt * np.random.normal(loc=0, scale=1, size=(rep, n))
    logpaths[:, 1:(n + 1)] = increments
    # 计算横向累加和, 包含了第一列的本金
    logpaths = np.cumsum(logpaths, axis=1)
    # 转换回普通形式
    spaths = np.exp(logpaths)
    return spaths


def ball_caskflow(s_0, paths, r_f, t, yields, up_b, low_b):
    """
    计算雪球的到期现金流，包含本金的收回

    - s_0: 资产初始价格
    - paths: 资产价格变动路径
    - r_f: 无风险利率
    - t: 时间（年），交易日每年252个，每月21个
    - n: 交易日总数
    - yields: 雪球约定的收益率
    - up_b: 敲出边界
    - low_b: 敲入边界
    观察日为：【21,42,63,...】，表现为 n % 21 == 0
    """
    payoff = []
    knock_out_times = 0
    knock_in_times = 0
    existence_times = 0
    for _ in paths:
        # 判断敲出
        tmp_out_day = np.where(_[:] > up_b * s_0)
        tmp_out_mon = tmp_out_day[0][tmp_out_day[0] % 21 == 0]  # 这里顺便完成了从tuplle到array的转换
        # 判断敲入
        tmp_in_day = np.where(_[:] < low_b * s_0)[0]  # 注意此时 np.whare 生成了一个tupple，储存日期信息的是第一个元素的array

        # 现金流分类讨论
        if len(tmp_out_mon) > 0:
            first_t = tmp_out_mon[0]
            payoff.append((yields * s_0 * (first_t / 252)) * np.exp(- r_f * first_t / 252))
            knock_out_times += 1
        elif len(tmp_out_mon) == 0 and len(tmp_in_day) == 0:
            payoff.append(yields * s_0 * np.exp(- r_f * t))
            existence_times += 1
        elif len(tmp_in_day) > 0 and len(tmp_out_mon) == 0:
            payoff.append(0 if _[-1] > s_0 else (_[-1] - s_0) * np.exp(- r_f * t))
            knock_in_times += 1
        else:
            return '数据错误'

    return payoff, knock_out_times, knock_in_times, existence_times


def draw_image(y):
    """
    画出资产价格的走势

    - y: 资产价格的array，价格横向变化
    """
    x = list(range(y.shape[1]))
    plt.style.use('default')  # 套用Style
    plt.rcParams['font.sans-serif'] = ['SimHei']  # 正常显示中文标签
    plt.rcParams['axes.unicode_minus'] = False  # 用来正常显示负号
    plt.figure(figsize=(6, 6))  # 画布大小
    for _ in y:
        plt.plot(x, _)
    plt.grid(visible=True, which='major', axis='both', linestyle='-.')  # 网格线
    plt.title('资产价格', loc='center')
    plt.xlabel('时间', loc='right')
    plt.ylabel('价格', loc='top')
    plt.show()
    plt.close()
    return None


def main():
    if __name__ == '__main__':
        np.random.seed(0)
        s_0 = 1.0
        upper_boundary = 1.03
        lower_boundary = 0.85
        t_year = 1
        sigma = 0.13
        r_f = 0.03
        yields = 0.2
        n = 252
        asset_array = simulate_path_vectorize(s_0=s_0, mu=r_f, sigma=sigma, t=1, n=n, rep=20000)
        po, kot, kit, et = ball_caskflow(s_0=s_0, paths=asset_array, r_f=r_f, t=t_year,
                                         yields=yields, up_b=upper_boundary, low_b=lower_boundary)
        print(f'雪球价格为：{np.array(po).mean()}')
        print(f'knock_out_times: {kot}')
        print(f'knock_in_times: {kit}')
        print(f'existence_times: {et}')
        draw_image(asset_array)


main()
