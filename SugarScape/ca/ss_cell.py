"""
Module containing the cell definition for the Sugarscape world.
"""

from cab.ca.cab_cell import CellHex

__author__ = 'Michael Wagner'
__version__ = '1.0'


class WorldCell(CellHex):
    def __init__(self, x, y, gc):
        super().__init__(x, y, gc)
        self.t_gen = None
        self.sugar = 0
        self.spice = 0
        self.max_sugar = 0
        self.max_spice = 0
        self.growth_cycle = 3
        self.growth_cycle_count = 0
        self.state = False

    def set_terrain_gen(self, tg):
        self.t_gen = tg
        self.sugar = int(self.t_gen.get(self.x, self.y))
        self.spice = int(self.gc.MAX_SUGAR - self.sugar)
        self.max_sugar = int(self.t_gen.get(self.x, self.y))
        self.max_spice = int(self.gc.MAX_SUGAR - self.sugar)
        # print("sugar: {0}, spice: {1}".format(self.sugar, self.spice))

    def clone(self, x, y):
        wc = WorldCell(x, y, self.gc)
        wc.set_terrain_gen(self.t_gen)
        return wc

    def sense_neighborhood(self):
        pass

    def update(self):
        if self.growth_cycle_count == self.growth_cycle:
            if self.sugar < self.max_sugar:
                self.sugar += 1
            if self.spice < self.max_spice:
                self.spice += 1
            self.growth_cycle_count = 0
        else:
            self.growth_cycle_count += 1