import numpy as np


class Node:
    def __init__(self, data):
        self.data = data
        self.child = []
        self.parent = None


def seg_item(item):
    """
    build a tree
    """
    k, v = '', ''
    f = Node((None, 0))
    p = f
    for i in item:
        i = str(i)
        if i.isupper():
            if k == '':
                k, v = i, ''
                continue
            if v == '':
                v = '1'
            c = Node((k, v))
            c.parent = p
            p.child.append(c)
            k, v = i, ''
        elif i.islower():
            k += i
        elif i.isdigit():
            v += i
        elif i == '(':
            if k == '':
                continue
            if v == '':
                v = '1'
            c = Node((k, v))
            c.parent = p
            p.child.append(c)
            p_ = Node((None, 0))
            p_.parent = p
            p = p_
            k, v = '', ''
        elif i == ')':
            if v == '':
                v = '1'
            c = Node((k, v))
            c.parent = p
            p.child.append(c)
            k, v = p, ''
            p = p.parent

    if k != '':
        if v == '':
            v = '1'
        c = Node((k, v))
        c.parent = p
        p.child.append(c)

    dic = {}
    a = [(f, 1)]
    while len(a) > 0:
        p, num = a.pop(0)
        for c in p.child:
            if isinstance(c.data[0], str):
                dic[c.data[0]] = dic.get(c.data[0], 0) + int(c.data[1]) * int(num)
            else:
                a.append(c.data)
    return dic


def level(left, right):
    lr = left + right
    lr_seg = []
    for item in lr:
        lr_seg.append(seg_item(item))

    a, b = set(), set()
    for i, j in enumerate(lr_seg):
        if i < len(left):
            a = a | set(j.keys())
        else:
            b = b | set(j.keys())
    if a != b:
        raise ValueError('left items do not equal to right items!')
    a, b = [_ for _ in a], [_ for _ in b]
    array = np.zeros((len(a), len(lr_seg) - 1), dtype=int)
    barray = np.zeros(len(a), dtype=int)
    for i in range(array.shape[0]):
        for j in range(array.shape[1] + 1):
            if j < len(left):
                array[i][j] = lr_seg[j].get(a[i], 0)
            elif j == array.shape[1]:
                barray[i] = lr_seg[j].get(a[i], 0)
            else:
                array[i][j] = -lr_seg[j].get(a[i], 0)

    if array.shape[0] > array.shape[1]:
        solve = np.linalg.solve(array[:array.shape[1], :], barray[:array.shape[1]])
    elif array.shape[0] < array.shape[1]:
        raise ValueError('chemical equation can not be leveled!')
    else:
        solve = np.linalg.solve(array, barray)
    for i in range(array.shape[0]):
        if barray[i] != 0:
            solve_ = array[i].dot(solve.reshape((-1, 1))) / barray[i]
            solve = np.hstack((solve, solve_))
            break
    i = 1
    while i < 100:
        solve = np.array(i / np.min(solve) * solve)
        for j in solve:
            q = np.abs(j - np.round(j))
            if q > 1e-4:
                break
        else:
            solve = np.array(np.round(solve), dtype=int)
            break
        i += 1
    return solve[:len(left)], solve[len(left):]


def get_text(left, right, left_solve, right_solve):
    text = ''
    for i, j in zip(left_solve, left):
        text += str(i) + j + ' + '
    text = text[:-3] + ' = '
    for i, j in zip(right_solve, right):
        text += str(i) + j + ' + '
    return text[:-3]


if __name__ == '__main__':
    # left, right = ('Fe2(SO4)3', 'NaOH'), ('Na2SO4', 'Fe(OH)3')
    # left, right = ('NH3', 'O2'), ('NO', 'H2O')
    # left, right = ('KMnO4', ), ('K2MnO4', 'MnO2', 'O2')
    # left, right = ('C2H6O4', 'O2'), ('CO2', 'SO2', 'H2O')
    # left, right = ('FeS2', 'O2'), ('Fe2O3', 'SO2')
    # left, right = ('C6H5CH3', 'KMnO4', 'H2SO4'), ('C6H5COOH', 'K2SO4', 'MnSO4', 'H2O')
    left, right = ('CH2OH(CHOH)4CHO', 'Ag(NH3)2OH'), ('CH2OH(CHOH)4COONH4', 'Ag', 'NH3', 'H2O')
    left_solve, right_solve = level(left, right)
    print('left: ' + str(left_solve) + ' right: ' + str(right_solve))
    print(get_text(left, right, left_solve, right_solve))
