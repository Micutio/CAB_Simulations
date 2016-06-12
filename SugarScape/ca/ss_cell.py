"""
Module containing the cell definition for the ant world.
"""

from cab.cab_global_constants import GlobalConstants
from cab.ca.cab_cell import CellHex
from util.ss_terrain_gen import TerrainGenerator

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

    def set_terrain_gen(self, tg):
        self.t_gen = tg
        self.sugar = int(self.t_gen.get(self.x, self.y))
        self.spice = int(self.gc.MAX_SUGAR - self.sugar)
        self.max_sugar = int(self.t_gen.get(self.x, self.y))
        self.max_spice = int(self.gc.MAX_SUGAR - self.sugar)

    def clone(self, x, y, c_size):
        wc = WorldCell(x, y, self.gc)
        wc.set_terrain_gen(self.t_gen)
        return wc

    def sense_neighborhood(self):
        pass

    def update(self):
        pass