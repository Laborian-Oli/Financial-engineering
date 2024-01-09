import numpy as np


def forward_p(current_p: int or float, r_f: float, t: int or float):
    """
    计算远期的价格
    - current_p: 资产的现值，整型或浮点
    - r_f: 无风险利率，浮点
    - t: 以无风险利率为标准的期数
    """
    r_0 = np.e ** (r_f * t)  # 无限套利条件下的本息和
    k = current_p * r_0
    return k


print(f'远期价格为：{forward_p(current_p=10, r_f=0.12, t=0.5)}')
