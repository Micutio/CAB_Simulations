
import math

from cab.util.rng import get_RNG

__author__ = 'Michael Wagner'
__version__ = '1.0'


class TerrainGenerator:
    def __init__(self, gc):
        self.width = gc.GRID_WIDTH
        self.height = gc.GRID_HEIGHT
        self.gc = gc
        self.highest = 10
        self.deepest = -10
        self.slope = 0.8
        self.smoothness = 3
        self.water_level = 0.0
        self.factor = 35
        self.landscape = {}
        self.landscape = self.get_coastal_landscape()

        # self.landscape = self.get_coastal_landscape()

    def get(self, x, y):
        # offset_x = int(self.width / 2)
        # offset_y = int(self.height / 2)
        try:
            # print('offset x: {0}, offset y:{1}, x: {2}, y: {3}'.format(offset_x, offset_y, x, y))
            return self.landscape[x, y]
        except KeyError:
            return 0
        except IndexError:
            return 0

    def get_coastal_landscape(self):
        l1 = {}
        l2 = {}
        for j in range(self.height):
            for i in range(self.width):
                # l1[i][j] = int(get_RNG().triangular(self.deepest, self.highest, 5))s
                q = i - math.floor(j / 2)
                mode = (((i + j) / 200) * 5) + self.water_level
                l1[q, j] = int(get_RNG().triangular(self.deepest + 2 * mode, self.highest + 2 * mode, mode))
                # l1[i][j] = int(get_RNG().triangular(self.deepest + 2 * mode, self.highest + 2 * mode, mode))

        for _ in range(self.smoothness):
            for j in range(self.height):
                for i in range(self.width):
                    q = i - math.floor(j / 2)
                    n = 0
                    f = 0
                    for d in self.gc.HEX_DIRECTIONS:
                        if not (d[0] == 0 and d[1] == 0):
                            try:
                                n += 1
                                f += l1[q + d[0], j + d[1]]
                            except KeyError:
                                pass
                    avg = f / n
                    if avg > l1[q, j]:
                        diff = avg - l1[q, j]
                        l2[q, j] = l1[q, j] + (diff * self.slope)
                    elif avg < l1[q, j]:
                        diff = l1[q, j] - avg
                        l2[q, j] = l1[q, j] - (diff * self.slope)
                    else:
                        l2[q, j] = l1[q, j]
            l1, l2 = l2, l1
        return l1

    def get_island_landscape(self):
        l1 = {}
        l2 = {}
        last_rand = 0
        for j in range(self.height):
            for i in range(self.width):
                q = i - math.floor(j / 2)
                if get_RNG().randint(0, 100) < self.factor:
                    c = get_RNG().choice([True, False])
                    if c:
                        # last_rand = int(get_RNG().triangular(self.deepest, self.highest, self.water_level))
                    # l1[q, j] = last_rand
                        l1[q, j] = self.highest
                        for d in self.gc.HEX_DIRECTIONS:
                            l1[q + d[0], j + d[1]] = int(get_RNG().triangular(self.water_level, self.highest, self.highest * 0.75))
                            # try:
                            #     l1[q + d[0], j + d[1]] = self.highest * 2
                            # except KeyError:
                            #     pass
                    else:
                        l1[q, j] = self.deepest
                        for d in self.gc.HEX_DIRECTIONS:
                            l1[q + d[0], j + d[1]] = int(get_RNG().triangular(self.deepest, self.water_level, self.deepest * 0.75))
                else:
                    l1[q, j] = self.water_level

        for _ in range(self.smoothness):
            for j in range(self.height):
                for i in range(self.width):
                    n = 0
                    f = 0
                    q = i - math.floor(j / 2)
                    for d in self.gc.HEX_DIRECTIONS:
                        if not (d[0] == 0 and d[1] == 0):
                            try:
                                n += 1
                                f += l1[q + d[0], j + d[1]]
                            except KeyError:
                                pass
                    avg = f / n
                    if avg > l1[q, j]:
                        diff = avg - l1[q, j]
                        l2[q, j] = l1[q, j] + (diff * self.slope)
                    elif avg < l1[q, j]:
                        diff = l1[q, j] - avg
                        l2[q, j] = l1[q, j] - (diff * self.slope)
                    else:
                        l2[q, j] = l1[q, j]
            l1, l2 = l2, l1
        return l1
