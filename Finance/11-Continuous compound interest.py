import math

import numpy as np
from matplotlib import pyplot as plt


r = 0.05
n = 10
conti_array = np.zeros(n)
no_conti_array = np.zeros(n)
x = np.linspace(1, n, n)


for _ in range(n):
    conti = math.pow(r + 1, 1 / (_ + 1)) - 1
    no_conti = r / (_ + 1)
    conti_array[_] = conti
    no_conti_array[_] = no_conti

error_array = (no_conti_array - conti_array) / conti_array  # 复利减去非复利


plt.style.use('default')  # 套用Style
plt.rcParams['font.sans-serif'] = ['SimHei']  # 正常显示中文标签
plt.rcParams['axes.unicode_minus'] = False  # 用来正常显示负号
plt.figure(figsize=(6, 6))  # 画布大小


plt.plot(x, conti_array, label='连续复利', linewidth=1, linestyle='-', marker='+', markersize=5)
plt.plot(x, no_conti_array, label='非复利', linewidth=1, linestyle='--', marker='.', markersize=5)
plt.bar(x, error_array, label='误差')

plt.legend(loc='best')

plt.grid(visible=True, which='major', axis='both', linestyle='-.')  # 网格线

plt.title('一年内利率的连续复利与非连续复利', loc='center')
plt.xlabel('X轴', loc='right')
plt.ylabel('Y轴', loc='top')

plt.show()
