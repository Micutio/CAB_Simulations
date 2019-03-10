
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
        self.factor = 70
        self.landscape = {}
        self.landscape = self.get_island_landscape()

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

    def get_color_for_terrain(self, cell):
        """
        Simple exemplary visualization. Draw cell in white.
        """
        if cell is None:
            return
        elif self.gc.CELL_VISUAL == "altitude":
            r = 0.0
            g = 0.0
            b = 0.0
            negative_height_offset = abs(self.deepest)
            if (negative_height_offset > 0.0):
                normalized = (cell.altitude + negative_height_offset) / (self.highest + negative_height_offset)
            else:
                normalized = (cell.altitude - self.deepest) / (self.highest - self.deepest)

            if normalized >= 0.0 and normalized <= 1.0 / 8.0:
                b = 4 * normalized + 0.5
            elif normalized > 1.0 / 8.0 and normalized <= 3.0 / 8.0:
                g = 3 * normalized - 0.5
                b = 1
            elif normalized > 3.0 / 8.0 and normalized <= 5.0 / 8.0:
                r = 4 * normalized - 1.5
                g = 1
                b = -4 * normalized + 2.5
            elif normalized > 5.0 / 8.0 and normalized <= 7.0 / 8.0:
                r = 1
                g = -4 * normalized + 3.5
            elif normalized > 7.0 / 8.0 and normalized <= 1.0:
                r = -4 * normalized + 4.5
            else:
                r = 0.8
                g = 0.8
                b = 0.8
            return (r * 255, g * 255, b * 255)
        elif self.gc.CELL_VISUAL == "air":
            blue = int(cell.air / 10 * 255)
            red = int(blue * 0.6)
            green = 0
        elif self.gc.CELL_VISUAL == "water":
            blue = green = int(cell.water / 10 * 255)
            red = 0
        elif self.gc.CELL_VISUAL == "light":
            red = green = int(cell.light / 10 * 255)
            blue = 0
        elif self.gc.CELL_VISUAL == "value":
            red = green = blue = int((cell.air + cell.water + cell.light) / 30 * 255)
        return (red, green, blue)
