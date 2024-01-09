def s(s_init, u, d, w: str = ''):
    """
    # 输入一个节点的价格编码，计算此时的资产价格

    - w: 从self.code中获取的一个'01'字符串
    """
    price = s_init
    for _ in w:
        if _ == '0':
            price = price * u
        elif _ == '1':
            price = price * d
        else:
            return '参数字符串错误'
    return price


class Option:
    """
    一个普通欧式期权的类，应用于多时段二叉树模型
    """

    def __init__(self, s_0, k, u, d, r, n):
        """
        - s_0: 标的物在时刻零的价格
        - k: 期权的执行价格
        - u: 上升因子
        - d: 下降因子
        - r: 单个时段的利率
        - n: 二叉树步数
        """
        self.s_0 = s_0
        self.k = k
        self.u = u
        self.d = d
        self.r = r
        self.n = n
        self.p = (u - r - 1) / (u - d)
        self.q = 1 - self.p
        # 二叉树每一个节点处资产价格S_n的自变量，'0'表示'H'，'1'表示'T'，结果按二叉树层数升序排列，每一层的资产价格按照生成结构排列。
        # 一个n时段的二叉树深度为n+1。
        # 输出一个元素是tuple，长度是(n+1)的tuple
        code_lsls = []
        for _ in range(n + 1):
            if _ == 0:
                code_ls = ['']
                code_lsls.append(tuple(code_ls))
            elif _ > 0:
                code_ls = []
                for __ in range(2 ** _):
                    code_ls.append(str(bin(__)).replace('0b', '', 1).rjust(_, '0'))
                code_lsls.append(tuple(code_ls))
            else:
                code_lsls = ['价格编码生成错误']
        self.code = tuple(code_lsls)
        # 下面是欧式期权支付的计算，子类期权需要重写
        v_bottom = []
        for _ in self.code[-1]:  # 这里计算了欧式期权到期时的支付，是递归算法的最底层
            v_bottom.append(max(s(self.s_0, self.u, self.d, _) - self.k, 0))
        self.v_bottom = v_bottom

    def v(self, n: int):
        """
        以递归的方式计算并输出任意一个时点的期权价格，返回一个list

        - n: 时刻数，也即二叉树的层数，从0开始
        - v(n)的值依赖于v(n+1)，除非n=self.n
        """
        v_ls = []
        if n == self.n:
            print('这是底层')
            return self.v_bottom
        elif n <= self.n:
            print(f'开始计算第{n}层')
            v_parent = self.v(n + 1)
            for _ in range(2 ** n):
                v = (self.p * v_parent[2 * _] + self.q * v_parent[2 * _ +1]) / (1 + self.r)
                v_ls.append(v)
            print(f'第{n}层计算完毕')
            return v_ls
        else:
            return '参数错误'


class AsianOption(Option):
    """
    亚式期权，继承自欧式期权
    """
    def __init__(self, s_0, k, u, d, r, n):
        super(AsianOption, self).__init__(s_0, k, u, d, r, n)
        # 只有期权支付需要重写，此时已经获得了现成的价格编码
        v_bottom = []
        # 先求出价格之和
        for _ in self.code[-1]:
            code = _[::-1]  # 字符串切片，步长为-1，实现翻转
            y = 1
            for __ in code:
                if __ == '0':
                    y = (y * self.u) + 1
                elif __ == '1':
                    y = (y * self.d) + 1
                else:
                    y = None
                    break
            y = y * self.s_0
            v_bottom.append(max((y / (self.n + 1) - self.k), 0))
        self.v_bottom = v_bottom

    def v_n(self, n, s_n, y):
        if n == self.n:
            v_output = max(y / (self.n + 1) - self.k, 0)
            return v_output
        elif n < self.n:
            v_output = (self.p * self.v_n(n+1, self.u * s_n, y + self.u * s_n) + self.q * self.v_n(n + 1, self.d * s_n, y + self.d * s_n)) / (1 + self.r)
            return v_output


if __name__ == '__main__':
    a = AsianOption(s_0=4, k=4, u=2, d=1 / 2, r=0.25, n=3)
    # print(a.v_bottom)
    print(a.v_n(0, 4, 4))
