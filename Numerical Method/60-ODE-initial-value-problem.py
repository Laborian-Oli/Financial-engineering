"""
 Author: 2020200229
 Creation time: 2022/11/13
 Filename: 60-ODE-homework
 """


def f_c(y, b=0.2, sig=0.05):
    y = b * y + (1 / 2) * (sig ** 2) * (y ** 2) - 1
    return y


def f_c_y(y, b=0.2, sig=0.05):  # 这是关于y的偏导，关于t的偏导因为没有用而没求
    fy = b + sig ** 2 * y
    return fy


def f_a(y, a=0.004):
    y = -a * y
    return y


def f_a_y(y, a=0.004):
    fy = -a
    return fy


def euler(func_c, func_a, c_t, a_t, h, T):  # 存储为两个list
    points_c = [c_t]
    points_a = [a_t]
    times = 0
    while True:
        if times != 50:
            a_t = a_t + func_a(c_t) * h  # 每次计算的A(t)只在下一次迭代的第一项用到
            c_t = c_t + func_c(c_t) * h  # C(t)的计算是正常的
            T += h
            times += 1
            points_c.append(c_t)
            points_a.append(a_t)
        elif times == 50:
            break
    return points_c, points_a


def taylor(func_c, func_a, func_c_y, func_a_y, c_t, a_t, h, T):
    points_c = [c_t]
    points_a = [a_t]
    times = 0
    while True:
        if times != 50:
            a_t = a_t + func_a(c_t) * h + (1 / 2) * (h ** 2) * (func_a(c_t) * func_a_y(c_t))
            c_t = c_t + func_c(c_t) * h + (1 / 2) * (h ** 2) * (func_c(c_t) * func_c_y(c_t))
            T += h
            times += 1
            points_c.append(c_t)
            points_a.append(a_t)
        else:
            break
    return points_c, points_a


def runkut(func_c, func_a, c_t, a_t, h, T):
    points_c = [c_t]
    points_a = [a_t]
    times = 0
    while True:
        if times != 50:
            a_t_adjust = c_t + (h / 2) * func_a(c_t)  # 这里使用的是c_t，就是C(t)，而不是A(t)
            a_t = a_t + h * func_a(a_t_adjust)
            c_t_adjust = c_t + (h / 2) * func_c(c_t)
            c_t = c_t + h * func_c(c_t_adjust)
            T += h
            times += 1
            points_c.append(c_t)
            points_a.append(a_t)
        else:
            break
    return points_c, points_a


def main():
    if __name__ == '__main__':
        T = 1
        h = -1 / 50
        c_t = 0
        a_t = 0
        x = [i / 100 for i in range(0, 101, 2)]
        euler_c_list, euler_a_list = euler(f_c, f_a, c_t, a_t, h, T)
        print(f'Euler法结果：\nC(0)={euler_c_list[-1]}, A(0)={euler_a_list[-1]}')
        taylor_c_list, taylor_a_list = taylor(f_c, f_a, f_c_y, f_a_y, c_t, a_t, h, T)
        print(f'Taylor法结果：\nC(0)={taylor_c_list[-1]}, A(0)={taylor_a_list[-1]}')
        # runkut(f_c, f_a, c_t, a_t, h, T)
        runkut_c_list, runkut_a_list = runkut(f_c, f_a, c_t, a_t, h, T)
        print(f'Runge-Kutta法结果：\nC(0)={runkut_c_list[-1]}, A(0)={runkut_a_list[-1]}')
        # euler_c_list, euler_a_list = euler(f_c, f_a, c_t, a_t, h, T)
        # print(euler_c_list)
        # print(euler_a_list)
        # taylor_c_list, taylor_a_list = taylor(f_c, f_a, f_c_y, f_a_y, c_t, a_t, h, T)
        # print(taylor_c_list)
        # print(taylor_a_list)
        # runkut_c_list, runkut_a_list = euler(f_c, f_a, c_t, a_t, h, T)
        # print(runkut_c_list)
        # print(runkut_a_list)
        # plt.figure(figsize=(16, 8), dpi=120)  # 图片大小和像素
        # plt.plot(x, euler_c_list)
        # plt.show()


main()
