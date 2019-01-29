"""https://github.com/MorvanZhou/sudoku"""

import numpy as np


def generate_sudoku(mask_rate=0.5):
    def recursion(m, r_, c_):
        m = np.array(m)
        for r in range(r_, 9):
            for c in range(c_, 9):
                col_rest = np.setdiff1d(rg, m[:r, c])
                row_rest = np.setdiff1d(rg, m[r, :c])
                avb1 = np.intersect1d(col_rest, row_rest)
                sub_r, sub_c = r // 3, c // 3
                avb2 = np.setdiff1d(np.arange(0, 9 + 1),
                                    m[sub_r * 3:(sub_r + 1) * 3, sub_c * 3:(sub_c + 1) * 3].ravel())
                avb = np.intersect1d(avb1, avb2)
                if len(avb) == 0:
                    return
                if len(avb) == 1:
                    m[r, c] = avb[0]
                    c_ = 0
                if len(avb) > 1:
                    np.random.shuffle(avb)
                    for i in avb:
                        m_ = m.copy()
                        m_[r, c] = i
                        if c == 9 - 1:
                            m_ = recursion(m_, r + 1, 0)
                        else:
                            m_ = recursion(m_, r, c + 1)
                        if m_ is not None and np.all(m_ != 0):
                            return m_
                    if m_ is None:
                        return
                # m[r, c] = np.random.choice(avb, size=1)
        return m

    m = np.zeros((9, 9), np.int)
    rg = np.arange(1, 9 + 1)
    m[0, :] = np.random.choice(rg, 9, replace=False)  # basic line
    m = recursion(m, 1, 0)
    mm = m.copy()
    # todo: playability is less
    mm[np.random.choice([True, False], size=m.shape, p=[mask_rate, 1 - mask_rate])] = 0
    return m, mm  # answer, problem


def solve(m):
    m = np.array(m)
    rg = np.arange(m.shape[0] + 1)
    while True:
        mt = m.copy()
        while True:
            d = []
            d_len = []
            for i in range(m.shape[0]):
                for j in range(m.shape[1]):
                    if mt[i, j] == 0:
                        """
                        a | b:
                            >>> np.intersect1d([1, 3, 4, 3], [3, 1, 2, 1])
                            array([1, 3])
                        
                        a & b:
                            >>> np.union1d([-1, 0, 1], [-2, 0, 2])
                            array([-2, -1,  0,  1,  2])
                        
                        a & b - b:
                            >>> a = np.array([1, 2, 3, 2, 4, 1])
                            >>> b = np.array([3, 4, 5, 6])
                            >>> np.setdiff1d(a, b)
                            array([1, 2])
                        """
                        possibles = np.setdiff1d(rg, np.union1d(np.union1d(mt[i, :], mt[:, j]),  # row and col remain
                                                                mt[3 * (i // 3):3 * (i // 3 + 1),  # Ix. Miyagi remain
                                                                3 * (j // 3):3 * (j // 3 + 1)]))
                        d.append([i, j, possibles])
                        d_len.append(len(possibles))
            if len(d) == 0:
                return mt
            idx = np.argmin(d_len)
            i, j, p = d[idx]
            if len(p) == 1:
                mt[i, j] = p[0]
            elif len(p) > 1:
                for k in p:
                    mt_ = mt.copy()
                    mt_[i, j] = k
                    mt_ = solve(mt_)
                    if mt_ is not None and np.all(mt_ != 0):
                        return mt_
                if mt_ is None:
                    return
            else:
                return


def check_solution(m):
    m = np.array(m)
    set_rg = set(np.arange(1, m.shape[0] + 1))
    for i in range(m.shape[0]):
        for j in range(m.shape[1]):
            r1 = set(m[3 * (i // 3):3 * (i // 3 + 1), 3 * (j // 3):3 * (j // 3 + 1)].ravel()) == set_rg
            r2 = set(m[i, :]) == set_rg
            r3 = set(m[:, j]) == set_rg
            if not (r1 and r2 and r3):
                break
        # for...else: if break in the cycle, don't jump into else method
        # so, when is passed, it jump into else method, and continue to next cycle
        # if isn't passed, it don't jump into else method, and break the cycle
        else:
            continue
        break
    else:
        return True
    return False


if __name__ == '__main__':
    np.random.seed(0)
    answer, problem = generate_sudoku()
    print('generate answer: ')
    print(answer)
    print('generate problem: ')
    print(problem)

    solution = solve(problem)
    print('solution: ')
    print(solution)
    print('check solution: ', end='')
    print(check_solution(solution))
    print('whether answer equals to solution: ', end='')
    print(np.all(answer == solution))
