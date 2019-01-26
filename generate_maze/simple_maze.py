"""https://indienova.com/indie-game-development/rooms-and-mazes-a-procedural-dungeon-generator/
https://www.cnblogs.com/WayneShao/p/5882680.html
"""

import numpy as np
from matplotlib import pyplot as plt
import matplotlib.animation as animation


class generator:
    def __init__(self, draw=False):
        self.draw = draw
        if self.draw:
            self.ims = []
            self.fig, self.ax = plt.subplots()
            self.ax.set_xticks([])
            self.ax.set_yticks([])

    def prim(self, h=10, w=10):
        # idx: even is path, odd is obstacles, value: 1 is path, 0 is obstacles
        m = np.zeros((h * 2 + 1, w * 2 + 1), dtype=bool)
        obstacles = {}
        start = (1, 1)
        obstacles[start] = [(1, 3), (3, 1)]  # {path: neighbours}
        m[1, 0] = m[start] = m[-2, -1] = 1
        while len(obstacles) > 0:
            i = np.random.randint(len(obstacles))
            path = list(obstacles.keys())[i]
            x, y = path
            neighbours = obstacles.get(path)
            next_path = neighbours[np.random.randint(len(neighbours))]
            x_, y_ = next_path
            if m[next_path] == 0:
                m[next_path] = 1
                m[x_ + (x - x_) // 2, y_ + (y - y_) // 2] = 1
                if self.draw:
                    self.show(m)
            neighbours.remove(next_path)
            if len(neighbours) == 0:  # if the path have no neighbours, pop it
                obstacles.pop(path)

            neighbours_ = obstacles.get(next_path, [])
            if len(neighbours_) == 0:
                if x_ > 1 and m[(x_ - 2, y_)] == 0:
                    neighbours_.append((x_ - 2, y_))
                if x_ < m.shape[0] - 2 and m[(x_ + 2, y_)] == 0:
                    neighbours_.append((x_ + 2, y_))
                if y_ > 1 and m[(x_, y_ - 2)] == 0:
                    neighbours_.append((x_, y_ - 2))
                if y_ < m.shape[1] - 2 and m[(x_, y_ + 2)] == 0:
                    neighbours_.append((x_, y_ + 2))
            if len(neighbours_) > 0:
                obstacles[next_path] = neighbours_

        return m

    def recursive_division(self, h=10, w=10):
        m = np.ones((h * 2 + 1, w * 2 + 1), dtype=bool)
        m[(0, -1), :] = m[:, (0, -1)] = 0
        m[1, 0] = m[-2, -1] = 1
        p = [(0, h, 0, w)]
        while len(p) > 0:
            minh, maxh, minw, maxw = p.pop(0)
            h0, w0, h1, w2 = minh, minw, minh, minw
            if minh + 1 < maxh:
                h0 = np.random.randint(minh + 1, maxh)
                m[h0 * 2, minw * 2:maxw * 2] = 0
                h1 = np.random.randint(h0, maxh)
                if self.draw:
                    self.show(m)
            if minw + 1 < maxw:
                w0 = np.random.randint(minw + 1, maxw)
                m[minh * 2:maxh * 2, w0 * 2] = 0
                w2 = np.random.randint(w0, maxw)
                if self.draw:
                    self.show(m)

            if h0 != minh:
                m[h0 * 2, w2 * 2 + 1] = 1
                if self.draw:
                    self.show(m)
            if w0 != minw:
                m[h1 * 2 + 1, w0 * 2] = 1
                if self.draw:
                    self.show(m)
            if minw < w0:
                w1 = np.random.randint(minw, w0)
                if h0 != minh:
                    m[h0 * 2, w1 * 2 + 1] = 1
                    if self.draw:
                        self.show(m)

            if m[minh:h0, minw:w0].size > 1:
                p.append((minh, h0, minw, w0))
            if m[minh:h0, w0:maxw].size > 1:
                p.append((minh, h0, w0, maxw))
            if m[h0:maxh, minw:w0].size > 1:
                p.append((h0, maxh, minw, w0))
            if m[h0:maxh, w0:maxw].size > 1:
                p.append((h0, maxh, w0, maxw))
        return m

    def recursive_backtracker(self, h, w):
        m = np.zeros((h * 2 + 1, w * 2 + 1), dtype=bool)
        dic = {0: (-2, 0), 1: (2, 0), 2: (0, -2), 3: (0, 2)}
        start = (1, 1)
        m[1, 0] = m[start] = m[-2, -1] = 1
        p = [start]

        while len(p) > 0:
            x, y = p[-1]
            l = list(range(4))
            np.random.shuffle(l)
            for i in l:
                dx, dy = dic[i]
                if 0 < x + dx < m.shape[0] and 0 < y + dy < m.shape[1] and m[(x + dx, y + dy)] != 1:
                    m[(x + dx, y + dy)] = m[(x + dx // 2, y + dy // 2)] = 1
                    p.append((x + dx, y + dy))
                    if self.draw:
                        self.show(m)
                    break
            else:
                p.pop(-1)
        return m

    def show(self, m):
        self.ims.append([self.ax.imshow(m)])


if __name__ == '__main__':
    gen = generator(draw=True)
    # maze = gen.prim(20, 10)
    #
    # ani = animation.ArtistAnimation(gen.fig, gen.ims, interval=100,
    #                                 repeat=True, repeat_delay=1000)
    # # ani.save('img/prim.gif', writer='imagemagick')
    # plt.show()
    #
    # # plt.imshow(maze)
    # # # plt.savefig('img/prim.png')
    # # plt.show()

    # maze = gen.recursive_division(10, 10)
    # ani = animation.ArtistAnimation(gen.fig, gen.ims, interval=100,
    #                                 repeat=True, repeat_delay=1000)
    # # ani.save('img/recursive_division.gif', writer='imagemagick')
    # plt.show()
    #
    # plt.imshow(maze)
    # # plt.savefig('img/recursive_division.png')
    # plt.show()

    maze = gen.recursive_backtracker(10, 10)
    ani = animation.ArtistAnimation(gen.fig, gen.ims, interval=100,
                                    repeat=True, repeat_delay=1000)
    # ani.save('img/recursive_backtracker.gif', writer='imagemagick')
    plt.show()

    plt.imshow(maze)
    # plt.savefig('img/recursive_backtracker.png')
    plt.show()
