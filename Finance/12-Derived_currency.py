def r(i_d, roun, r_d, r_t, t):
    """
    计算活期和定期区分情况下的存款货币创造

    - i_d: 初始存款
    - roun: 创造轮次
    - r_d: 活期存款的准备金率
    - r_t: 定期存款的准备金率
    - t: 定期存款与活期存款之比
    """
    if roun == 0:
        return i_d
    elif roun == 1:
        r_prior = i_d
    elif roun > 1:
        r_prior = r(i_d, roun - 1, r_d, r_t, t)
    else:
        return '轮次错误'
    delta_d = (r_prior / (1 + t)) * (1 - r_d)
    delta_t = t * (r_prior / (1 + t)) * (1 - r_t)

    return delta_d + delta_t


d_total = 0
for _ in range(100):
    d_total += r(i_d=100, roun=_, r_d=0.2, r_t=0.1, t=0.5)

print(d_total)

r_formula = (100 / (0.2 + 0.1 * 0.5)) * (1 + 0.5)
print(r_formula)
