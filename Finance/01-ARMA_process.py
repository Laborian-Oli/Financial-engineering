"""
 Author: 2020200229
 Creation time: 2023/3/26
 Filename: 01-ARMA_process
 """
class ARMA:
    def __init__(self, ar: list = None, ma: list = None, c: int or float = 0):
        """
        ar: AR过程的系数列表或元组
        ma: MA过程的系数列表或元组
        c: 常数项
        """
        self.ar = [] if ar is None else  ar
        self.ma = [] if ma is None else  ma
        self.c = c
    # 这里缺乏验证平稳性和可逆性的方法