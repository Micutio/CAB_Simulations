"""
Main module of the Gol and Pressure Demo.
Uses the Complex Automaton Base.
"""

# External library imports.
import pygame
import random

# CAB system imports.
from cab.ca.cab_cell import CellRect
from cab.cab_global_constants import GlobalConstants
from cab.cab_system import ComplexAutomaton
from cab.util.cab_input_handling import InputHandler
from cab.util.cab_visualization import Visualization


__author__ = 'Michael Wagner'
__version__ = '1.0'


class GC(GlobalConstants):
    def __init__(self):
        super().__init__()
        self.VERSION = 'version: 08-2015'
        ################################
        #     SIMULATION CONSTANTS     #
        ################################
        self.RUN_SIMULATION = False
        self.ONE_AGENT_PER_CELL = False
        ################################
        #         CA CONSTANTS         #
        ################################
        self.USE_HEX_CA = False
        self.USE_MOORE_NEIGHBORHOOD = True
        self.USE_CA_BORDERS = True
        self.DIM_X = 50  # How many cells is the ca wide?
        self.DIM_Y = 50  # How many cells is the ca high?
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

        if self.alive == 0 and _neighs_alive in self.b:
            self.next_state = 1
        elif self.alive == 1 and _neighs_alive in self.s:
            self.next_state = 1
        else:
            self.next_state = 0

    def update(self):
        self.alive = self.next_state

    def clone(self, x, y):
        return GolCell(x, y, self.gc)


class GolIO(InputHandler):
    def __init__(self, cab_sys):
        super().__init__(cab_sys)

    def clone(self, cab_sys):
        return GolIO(cab_sys)

    def custom_mouse_action(self, button):
        # Click on left mouse button.
        if button == 1:
            cell_x, cell_y = self.get_mouse_hex_coords()
            self.sys.ca.ca_grid[cell_x, cell_y].alive = 1 - self.sys.ca.ca_grid[cell_x, cell_y].alive

        # Click on middle mouse button / mouse wheel, not used here
        # elif button == 2:

        # Click on right mouse button
        elif button == 3:
            for cell in list(self.sys.ca.ca_grid.values()):
                if random.random() > 0.65:
                    cell.alive = 1
                else:
                    cell.alive = 0


class GolVis(Visualization):
    def __init__(self, global_const, sys,  screen):
        super().__init__(global_const, sys, screen)

    def clone(self, cab_sys, screen):
        return GolVis(self.gc, cab_sys, screen)

    def draw_cell(self, cell):
        """
        Simple exemplary visualization. Draw cell in white.
        """
        if cell is None:
            pass
        else:
            if cell.is_border:
                pygame.gfxdraw.filled_polygon(self.surface, cell.get_corners(), (190, 190, 190))
            else:
                if cell.alive:
                    red = 0
                    green = 0
                    blue = 0
                else:
                    red = 255
                    green = 255
                    blue = 255
                pygame.gfxdraw.filled_polygon(self.surface, cell.get_corners(), (red, green, blue))
                pygame.gfxdraw.aapolygon(self.surface, cell.get_corners(), (190, 190, 190))


if __name__ == '__main__':
    gc = GC()
    pc = GolCell(0, 0, gc)
    ph = GolIO(None)
    pv = GolVis(gc, None, None)
    simulation = ComplexAutomaton(gc, proto_cell=pc, proto_handler=ph, proto_visualizer=pv)
    simulation.run_main_loop()
    # cProfile.run("simulation.run_main_loop()")
