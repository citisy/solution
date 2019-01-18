"""https://www.zhihu.com/question/22625187
探索微信抢红包的算法
"""

import numpy as np


def solve(money, pers):
    money = int(money * 100)  # solve the accuracy issues of float type
    a = []
    money_, pers_ = money, pers
    for i in range(pers - 1):
        if money_ == pers_:
            b = 1
        else:
            b = np.random.randint(1, money_ // pers_ * 2 + 1)
        a.append(b)
        money_ -= b
        pers_ -= 1
    a.append(money - sum(a))
    return [i / 100 for i in a]


if __name__ == '__main__':
    for i in range(100):
        np.random.seed(i)
        a = solve(0.1, 9)
        print(i, a)
