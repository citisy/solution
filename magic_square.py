"""https://jingyan.baidu.com/article/c85b7a64bc0086003bac95a3.html"""

import numpy as np


def solve(nums, n):
    def solve_(m, nums):
        for i, j in enumerate(nums):
            if len(m) < n * n:
                m_, nums_ = m.copy(), nums.copy()
                m_.append(nums_.pop(i))
                if len(nums_) > 0:
                    ma = solve_(m_, nums_)
                    if ma is not None:
                        return ma
                else:
                    ma = np.array(m_, dtype=int).reshape((n, n))
                    a = np.hstack((
                        np.sum(ma, axis=0),
                        np.sum(ma, axis=1),
                        np.sum(ma[range(n), range(n)]),
                        np.sum(ma[range(n), range(n - 1, -1, -1)])
                    ))
                    if np.all(a == a[0]):
                        return ma
                    else:
                        return

    if len(nums) != n * n:
        raise ValueError('nums size do not match n * n')
    m = []
    m_, nums_ = m.copy(), nums.copy()
    return solve_(m, nums_)


if __name__ == '__main__':
    import time

    n = 3
    st = time.time()
    ma = solve(list(range(1, n * n + 1)), n)
    et = time.time()
    print(ma)
    print(et - st)

"""
Violent cracking is very slow
n = 3, use time: 4.289s
"""
