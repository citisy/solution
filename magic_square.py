import numpy as np


def solve(nums, n, method='violent'):
    if len(nums) != n * n:
        raise ValueError('nums size do not match n * n')
    if method == 'violent':
        return violent_solve(nums, n)
    elif method == 'smart':
        if n % 4 == 0:
            return maze_with_4times_solve(nums, n)
        elif n % 2 == 0:
            return even_solve(nums, n)
        else:
            return odd_solve(nums, n)


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
                    if check_solution(ma, n):
                        return ma
                    else:
                        return

    m = []
    m_, nums_ = m.copy(), nums.copy()
    return solve_(m, nums_)


def odd_solve(nums, n):
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


def even_solve(nums, n):
    ma = np.zeros((n, n), dtype=int)
    k = (n - 2) // 4
    n_ = n // 2
    dic = {0: (0, 0), 1: (1, 1), 2: (0, 1), 3: (1, 0)}
    m = []
    for i in range(4):
        m.append(solve(nums[n_ * n_ * i:n_ * n_ * (i + 1)], n_, method='smart'))

    for i in range(n_):
        for j in range(n_):
            if (j < k and i != n_ // 2) or (k <= j < n_ - 1 and i == n_ // 2):
                m[0][(i, j)], m[3][(i, j)] = m[3][(i, j)], m[0][(i, j)]
            if n_//2 - k + 1 < j < n_//2 + 1:
                m[1][(i, j)], m[2][(i, j)] = m[2][(i, j)], m[1][(i, j)]
    for i in range(4):
        x, y = dic[i]
        ma[x * n_:(x + 1) * n_, y * n_: (y + 1) * n_] = m[i]
    return ma


def maze_with_4times_solve(nums, n):
    ma = np.array(nums, dtype=int).reshape((n, n))
    ma_ = ma.copy()
    su = max(nums) + min(nums)
    for x in range(n // 4):
        for y in range(n//4):
            m = ma[x * 4:(x + 1) * 4, y * 4:(y + 1) * 4]
            # m_ = ma_[(n // 4 - k - 1) * 4:(n // 4 - k) * 4, (n // 4 - k - 1) * 4:(n // 4 - k) * 4]
            m_ = ma_[x * 4:(x + 1) * 4, y * 4:(y + 1) * 4]
            for i in range(4):
                # m[i, i] = m_[4 - i - 1, 4 - i - 1]
                # m[4 - i - 1, i] = m_[i, 4 - i - 1]
                m[i, i] = su - m_[i, i]
                m[4 - i - 1, i] = su - m_[4 - i - 1, i]

            m = ma[x * 4:(x + 1) * 4, (n // 4 - y - 1) * 4:(n // 4 - y) * 4]
            m_ = ma_[x * 4:(x + 1) * 4, (n // 4 - y - 1) * 4:(n // 4 - y) * 4]
            # m_ = ma_[(n // 4 - k - 1) * 4:(n // 4 - k) * 4, k * 4:(k + 1) * 4]
            for i in range(4):
                # m[i, i] = m_[4 - i - 1, 4 - i - 1]
                # m[4 - i - 1, i] = m_[i, 4 - i - 1]
                m[i, i] = su - m_[i, i]
                m[4 - i - 1, i] = su - m_[4 - i - 1, i]
    return ma


def check_solution(ma, n):
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
    # import time
    # st = time.time()
    # n = 3
    # solution = solve(list(range(1, n * n + 1)), n, method='violent')
    # et = time.time()
    # print(solution)
    # print(check_solution(solution, n))
    # print(et - st)

    for n in range(3, 100):
        solution = solve(list(range(1, n * n + 1)), n, method='smart')
        print(n, check_solution(solution, n))



"""
Violent cracking is very slow
n = 2, use time: 0.001s
n = 3, use time: 4.289s
n = 5, use time: very very long =_=! 
all the possible is 25! and 9! use 4s
Smart method please refer to:
https://www.cnblogs.com/codingmylife/archive/2010/12/24/1915728.html
"""
