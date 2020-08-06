"""https://www.cnblogs.com/WayneShao/p/5882680.html
https://bost.ocks.org/mike/algorithms/#maze-generation"""

import numpy as np
from matplotlib import pyplot as plt
import matplotlib.animation as animation
import matplotlib.colors as colors
from matplotlib.animation import FFMpegWriter as Writer


class MazeGenerator:
    def __init__(self, collect_picture=False):
        self.collect_picture = collect_picture

    def gen(self, h, w, start, end):
        """生成辅助数组
        m: 偶数下标是墙壁域，奇数下标是路径域；值为假为墙壁，置为真为路径"""
        start = start or (0, 0)
        end = end or (h, w)
        m = np.zeros((h * 2 + 1, w * 2 + 1), dtype=bool)

        # 起点和终点
        m[start[0], start[1] + 1] = 1
        m[start[0] + 1, start[1] + 1] = 1
        m[2 * end[0], 2 * end[1] - 1] = 1

        n = h * w
        flag = np.zeros(n, dtype=bool)
        arr = np.zeros((n, n), dtype=bool)

        # 构建图
        for i in range(n):
            if i % w > 0:
                arr[i, i - 1] = 1
            if i % w < w - 1:
                arr[i, i + 1] = 1
            if i >= w:
                arr[i, i - w] = 1
            if i < n - w:
                arr[i, i + w] = 1

        return m, arr, flag, start, end

    def BFS(self, h=10, w=10, start=None, end=None, draw_args=dict()):
        """随机广度优先遍历"""
        if self.collect_picture:
            self.draw_initialize()

        m, arr, flag, start, end = self.gen(h, w, start, end)

        iu = start[0] * w + start[1]
        queue = [iu]
        flag[iu] = 1
        while queue:
            iu = queue.pop(0)
            ivs = np.where(arr[iu] == 1)[0]
            np.random.shuffle(ivs)
            for iv in ivs:
                if not flag[iv]:
                    i0, j0 = iu // w, iu % w
                    i1, j1 = iv // w, iv % w
                    if i0 == i1:
                        m[2 * i0 + 1, 2 * max(j0, j1)] = 1
                    else:
                        m[2 * max(i0, i1), 2 * j0 + 1] = 1
                    m[2 * i1 + 1, 2 * j1 + 1] = 1

                    if self.collect_picture:
                        self.collect_pic(m)

                    flag[iv] = 1
                    queue.append(iv)

        if self.collect_picture:
            self.show(m, draw_args)

        return m

    def DFS(self, h=10, w=10, start=None, end=None, draw_args=dict()):
        """随机深度优先遍历"""

        def recursive(iu):
            flag[iu] = 1
            ivs = np.where(arr[iu] == 1)[0]
            np.random.shuffle(ivs)
            for iv in ivs:
                if not flag[iv]:
                    i0, j0 = iu // w, iu % w
                    i1, j1 = iv // w, iv % w
                    if i0 == i1:
                        m[2 * i0 + 1, 2 * max(j0, j1)] = 1
                    else:
                        m[2 * max(i0, i1), 2 * j0 + 1] = 1
                    m[2 * i1 + 1, 2 * j1 + 1] = 1

                    if self.collect_picture:
                        self.collect_pic(m)

                    recursive(iv)

        if self.collect_picture:
            self.draw_initialize()

        m, arr, flag, start, end = self.gen(h, w, start, end)

        iu = start[0] * w + start[1]

        recursive(iu)

        if self.collect_picture:
            self.show(m, draw_args)

        return m

    def prim(self, h=10, w=10, start=None, end=None, draw_args=dict()):
        """随机生成树"""

        if self.collect_picture:
            self.draw_initialize()

        m, arr, flag, start, end = self.gen(h, w, start, end)
        iu = start[0] * w + start[1]
        flag[iu] = 1

        while 0 in flag:
            cache = []
            for iu in np.where(flag == 1)[0]:
                for iv in np.where(arr[iu, :] == 1)[0]:
                    if not flag[iv]:
                        cache.append((iu, iv))

            i = np.random.randint(len(cache))
            iu, iv = cache[i]
            flag[iv] = 1

            i0, j0 = iu // w, iu % w
            i1, j1 = iv // w, iv % w
            if i0 == i1:
                m[2 * i0 + 1, 2 * max(j0, j1)] = 1
            else:
                m[2 * max(i0, i1), 2 * j0 + 1] = 1
            m[2 * i1 + 1, 2 * j1 + 1] = 1

            if self.collect_picture:
                self.collect_pic(m)

        if self.collect_picture:
            self.show(m, draw_args)

        return m

    def recursive_division(self, h=10, w=10, start=None, end=None, draw_args=dict()):
        """递归分割
        虽然说是递归的，但这里我用的是循环，hhh"""

        if self.collect_picture:
            self.draw_initialize()

        start = start or (0, 0)
        end = end or (h, w)

        m = np.ones((h * 2 + 1, w * 2 + 1), dtype=bool)
        m[(0, -1), :] = m[:, (0, -1)] = 0

        # 起点和终点
        m[start[0], start[1] + 1] = 1
        m[start[0] + 1, start[1] + 1] = 1
        m[2 * end[0], 2 * end[1] - 1] = 1

        p = [(0, h, 0, w)]
        while p:
            minh, maxh, minw, maxw = p.pop(0)
            h0, w0, h1, w2 = minh, minw, minh, minw
            if minh + 1 < maxh:     # 中间横边
                h0 = np.random.randint(minh + 1, maxh)
                m[h0 * 2, minw * 2:maxw * 2] = 0
                h1 = np.random.randint(h0, maxh)
                if self.collect_picture:
                    self.collect_pic(m)

            if minw + 1 < maxw:     # 中间竖边
                w0 = np.random.randint(minw + 1, maxw)
                m[minh * 2:maxh * 2, w0 * 2] = 0
                w2 = np.random.randint(w0, maxw)
                if self.collect_picture:
                    self.collect_pic(m)

            if h0 != minh:      # 横边右半部分打通
                m[h0 * 2, w2 * 2 + 1] = 1
                if self.collect_picture:
                    self.collect_pic(m)

            if w0 != minw:      # 竖边上半部分打通
                m[h1 * 2 + 1, w0 * 2] = 1
                if self.collect_picture:
                    self.collect_pic(m)

            if minw < w0:       # 横边左半部分打通
                w1 = np.random.randint(minw, w0)
                if h0 != minh:
                    m[h0 * 2, w1 * 2 + 1] = 1
                    if self.collect_picture:
                        self.collect_pic(m)

            if m[minh:h0, minw:w0].size > 1:
                p.append((minh, h0, minw, w0))
            if m[minh:h0, w0:maxw].size > 1:
                p.append((minh, h0, w0, maxw))
            if m[h0:maxh, minw:w0].size > 1:
                p.append((h0, maxh, minw, w0))
            if m[h0:maxh, w0:maxw].size > 1:
                p.append((h0, maxh, w0, maxw))

        if self.collect_picture:
            self.show(m, draw_args)

        return m

    def draw_initialize(self):
        self.ims = []
        self.fig, self.ax = plt.subplots()
        self.ax.set_axis_off()
        self.cmap = colors.ListedColormap(['black', 'white'])

    def collect_pic(self, m):
        self.ims.append([self.ax.imshow(m, cmap=self.cmap)])

    def show(self, m, draw_args):
        ani = animation.ArtistAnimation(self.fig, self.ims, interval=100,
                                        repeat=True, repeat_delay=1000)

        if draw_args.get('save_ani', None):
            ani.save(draw_args['save_ani'], writer=Writer(fps=50))

        if draw_args.get('show_ani', None):
            plt.show()

        fig, ax = plt.subplots()
        ax.imshow(m, cmap=self.cmap)

        if draw_args.get('save_result', None):
            plt.savefig(draw_args['save_result'])

        if draw_args.get('show_result', None):
            plt.show()


if __name__ == '__main__':
    np.random.seed(0)
    gen = MazeGenerator(collect_picture=True)

    gen.BFS(20, 20,
            draw_args={
                'show_ani': False,
                'save_ani': 'img/BFS.mp4',
                'show_result': True,
                'save_result': 'img/BFS.png'
            })

    gen.DFS(20, 20,
            draw_args={
                'show_ani': False,
                'save_ani': 'img/DFS.mp4',
                'show_result': True,
                'save_result': 'img/DFS.png'
            })

    gen.prim(20, 20,
             draw_args={
                 'show_ani': False,
                 'save_ani': 'img/prim.mp4',
                 'show_result': True,
                 'save_result': 'img/prim.png'
             })

    gen.recursive_division(20, 20,
                           draw_args={
                               'show_ani': False,
                               'save_ani': 'img/recursive_division.mp4',
                               'show_result': True,
                               'save_result': 'img/recursive_division.png'
                           })
