import numpy as np


def solve(nums, n, method='violent'):
    if len(nums) != n * n:
        raise ValueError('nums size do not match n * n')
    if method == 'violent':
        return violent_solve(nums, n)
    elif method == 'smart':
        if n % 2 == 0:
            raise ValueError('do not support even square!')
        else:
            return smart_solve(nums, n)


def violent_solve(nums, n):
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
                    if check_solution(ma):
                        return ma
                    else:
                        return
    m = []
    m_, nums_ = m.copy(), nums.copy()
    return solve_(m, nums_)


def smart_solve(nums, n):
    ma = np.zeros((n, n), dtype=int)
    i, j = 0, ma.shape[1] // 2
    for a in range(n * n):
        if a != 0:
            i_, j_ = i - 1, j + 1
            if j_ == ma.shape[0]:
                j_ = 0
            if i_ == -1:
                i_ = ma.shape[1] - 1
            if ma[i_, j_] != 0:
                i_, j_ = i + 1, j
            i, j = i_, j_
        ma[i, j] = nums[a]
    return ma


def check_solution(ma):
    a = np.hstack((
        np.sum(ma, axis=0),
        np.sum(ma, axis=1),
        np.sum(ma[range(n), range(n)]),
        np.sum(ma[range(n), range(n - 1, -1, -1)])
    ))
    if np.all(a == a[0]):
        return True
    else:
        return False


if __name__ == '__main__':
    import time

    n = 3
    st = time.time()
    ma = solve(list(range(1, n * n + 1)), n, method='smart')
    et = time.time()
    print(ma)
    print(check_solution(ma))
    print(et - st)

"""
Violent cracking is very slow
n = 2, use time: 0.001s
n = 3, use time: 4.289s
n = 5, use time: very very long =_=! 
all the possible is 25! and 9! use 4s
Smart method please refer to:
https://jingyan.baidu.com/article/c85b7a64bc0086003bac95a3.html
"""
