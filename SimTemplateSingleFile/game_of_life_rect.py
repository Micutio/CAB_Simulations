"""
Main module of the Gol and Pressure Demo.
Uses the Complex Automaton Base.
"""

# External library imports.
import pygame

# CAB system imports.
from cab.ca.cab_cell import CellRect
from cab.cab_global_constants import GlobalConstants
from cab.cab_system import ComplexAutomaton
import cab.util.cab_rng


__author__ = 'Michael Wagner'
__version__ = '1.0'


class GC(GlobalConstants):
    def __init__(self):
        super().__init__()
        self.VERSION = 'version: 07-2017'
        ################################
        #     SIMULATION CONSTANTS     #
        ################################
        self.RUN_SIMULATION = False
        self.ONE_AGENT_PER_CELL = False
        ################################
        #         CA CONSTANTS         #
        ################################
        self.DISPLAY_GRID = True
        self.USE_HEX_CA = False
        self.USE_MOORE_NEIGHBORHOOD = True
        self.USE_CA_BORDERS = True
        self.DIM_X = 100  # How many cells is the ca wide?
        self.DIM_Y = 100  # How many cells is the ca high?
        self.CELL_SIZE = 10  # How long/wide is one cell?
        self.GRID_WIDTH = self.DIM_X * self.CELL_SIZE
        self.GRID_HEIGHT = self.DIM_Y * self.CELL_SIZE
        ################################
        #        ABM CONSTANTS         #
        ################################
        ################################
        #      UTILITY CONSTANTS       #
        ################################


class GolCell(CellRect):
    def __init__(self, x, y, global_const):
        super().__init__(x, y, global_const)
        self.alive = 0
        self.next_state = 0
        # The rules:
        #   cell will be [b]orn if number of alive_neighbors is in self.b
        self.b = [2]
        #   cell will [s]tay alive if number of alive_neighbors is in self.s
        self.s = [3, 4]

    def sense_neighborhood(self):
        _neighs_alive = 0
        for cell in self.neighbors:
            if cell.alive == 1 and not cell.is_border:
                _neighs_alive += 1

        if not self.alive and _neighs_alive in self.b:
            self.next_state = 1
        elif self.alive and _neighs_alive in self.s:
            self.next_state = 1
        else:
            self.next_state = 0

    def update(self):
        self.alive = self.next_state
        if self.alive:
            self.color = (255, 255, 255)
        else:
            self.color = self.gc.DEFAULT_CELL_COLOR

    def clone(self, x, y):
        return GolCell(x, y, self.gc)

    def on_lmb_click(self, abm, ca):
        self.alive = True
        self.color = (255, 255, 255)

    def on_rmb_click(self, abm, ca):
        self.alive = False
        self.color = (0, 0, 0)

if __name__ == '__main__':
    gc = GC()
    pc = GolCell(0, 0, gc)
    simulation = ComplexAutomaton(gc, proto_cell=pc)
    simulation.run_main_loop()
    # cProfile.run("simulation.run_main_loop()")
