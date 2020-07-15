import numpy as np


class Node:
    def __init__(self, data, parent=None):
        self.data = data
        self.child = []
        self.parent = parent


def get_node(p, k, v):
    v = v or '1'  # 如果没有标明数量，则默认为1
    c = Node([k, v], p)
    p.child.append(c)


def seg_item(item):
    """build a tree"""
    k, v = '', ''
    f = Node((None, 1))
    p = f
    for i in item:
        i = str(i)
        if i.isupper():  # 遇到了一个新的元素
            if k == '':  # 上一元素已经被缓存了
                k, v = i, ''
                continue

            get_node(p, k, v)
            k, v = i, ''

        elif i.islower():
            k += i

        elif i.isdigit():
            v += i

        elif i == '(':
            if k == '':
                continue

            get_node(p, k, v)
            k, v = '', ''

            # 遇到左括号，向下移一层
            p_ = Node((None, 1))
            p_.parent = p
            p = p_

        elif i == ')':
            get_node(p, k, v)
            k, v = p, ''  # 缓存主节点
            p = p.parent  # 遇到右括号，向上移一层

    if k != '':
        get_node(p, k, v)

    dic = {}
    a = [(f, 1)]
    while a:
        p, num = a.pop(0)
        for c in p.child:
            c.data[1] = int(c.data[1]) * int(num)
            if isinstance(c.data[0], str):
                dic[c.data[0]] = dic.get(c.data[0], 0) + c.data[1]
            else:
                a.append(c.data)

    return dic


def balance(left, right):
    lr = left + right
    lr_seg = []
    for item in lr:
        lr_seg.append(seg_item(item))

    l, r = set(), set()
    for i, dic in enumerate(lr_seg):
        if i < len(left):
            l |= set(dic.keys())
        else:
            r |= set(dic.keys())

    if l != r:
        raise ValueError('Left items do not equal to right items!')

    l, r = list(l), list(r)

    arr = np.zeros((len(l), len(lr_seg)), dtype=int)

    for i in range(arr.shape[0]):
        for j in range(arr.shape[1]):
            if j < len(left):  # 左边元素录入
                arr[i][j] = lr_seg[j].get(l[i], 0)
            else:  # 右边元素取负录入
                arr[i][j] = -lr_seg[j].get(l[i], 0)

    if arr.shape[0] >= arr.shape[1]:
        a, b = arr[:arr.shape[1] - 1, :-1], -arr[:arr.shape[1] - 1, -1]
    elif arr.shape[0] < arr.shape[1] - 1:
        raise ValueError('Chemical equation can not be balanced!')
    else:
        a, b = arr[:, :-1], -arr[:, -1]

    solve = np.linalg.solve(a, b)   # 通解

    for i in range(a.shape[0]):  # 特解
        if b[i] != 0:
            solve_ = a[i].dot(solve.reshape((-1, 1))) / b[i]
            solve = np.hstack((solve, solve_))
            break

    # 小数取整，这里用的是暴力遍历法
    # 这里不先把小数转为分数后再求其最大公约树，因为比较难把无限循环小数化为分数
    i = 1
    while i < 100:
        solve_ = np.array(i / np.min(solve) * solve)
        for j in solve_:
            if np.abs(j - np.round(j)) > 1e-4:  # 如果不能化成整数，就退出进行下一个数
                break
        else:
            solve = np.array(np.round(solve_), dtype=int)
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
    # left, right = ('KMnO4', 'H2O2', 'H2SO4'), ('K2SO4', 'MnSO4', 'O2', 'H2O')
    # left, right = ('C6H12O6', 'O2'), ('CO2', 'H2O')
    # left, right = ('FeS2', 'O2'), ('Fe2O3', 'SO2')
    # left, right = ('C6H5CH3', 'KMnO4', 'H2SO4'), ('C6H5COOH', 'K2SO4', 'MnSO4', 'H2O')
    left, right = ('CH2OH(CHOH)4CHO', 'Ag(NH3)2OH'), ('CH2OH(CHOH)4COONH4', 'Ag', 'NH3', 'H2O')
    left_solve, right_solve = balance(left, right)
    print('left: ' + str(left_solve) + ' right: ' + str(right_solve))
    print(get_text(left, right, left_solve, right_solve))
