"""
Main module of the Gol and Pressure Demo.
Uses the Complex Automaton Base.
"""

from cab.ca.cab_cell import CellHex
from cab.cab_global_constants import GlobalConstants
from cab.cab_system import ComplexAutomaton
from cab.util.cab_input_handling import InputHandler
from cab.util.cab_visualization import Visualization

import pygame
import math
import random

__author__ = 'Michael Wagner'


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
        self.USE_HEX_CA = True
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


class GolCell(CellHex):
    def __init__(self, x, y, c_size, c):
        super().__init__(x, y, c_size, c)
        self.alive = 0
        self.next_state = 0
        # The rules:
        #   cell will be [b]orn if it has the following amount of neighbors
        self.b = [2]
        #   cell will [s]tay alive if it has the following amount of neighbors
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

    def get_mouse_hex_coords(self):
        _q = (self.mx * math.sqrt(3)/3 - self.my/3)  # / self.sys.gc.CELL_SIZE
        _r = self.my * 2/3  # / self.sys.gc.CELL_SIZE
        cell_q, cell_r = hex_round(_q, _r)
        return cell_q, cell_r

    def custom_mouse_action(self, button):
        # Click on left mouse button.
        if button == 1:
            cell_x, cell_y = self.get_mouse_hex_coords()
            self.sys.ca.ca_grid[cell_x, cell_y].alive = 1 - self.sys.ca.ca_grid[cell_x, cell_y].alive

        # Click on middle mouse button / mouse wheel. Not used here.
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
                pygame.gfxdraw.filled_polygon(self.surface, cell.get_corners(), (120, 120, 120))
            else:
                if cell.alive:
                    red = 90
                    green = 90
                    blue = 90
                else:
                    red = 220
                    green = 220
                    blue = 220
                pygame.gfxdraw.filled_polygon(self.surface, cell.get_corners(), (red, green, blue))
                pygame.gfxdraw.aapolygon(self.surface, cell.get_corners(), (190, 190, 190))


def hex_round(q, r):
    return cube_to_hex(*cube_round(*hex_to_cube(q, r)))


def cube_round(x, y, z):
    rx = round(x)
    ry = round(y)
    rz = round(z)
    dx = abs(rx - x)
    dy = abs(ry - y)
    dz = abs(rz - z)

    if dx > dy and dx > dz:
        rx = -ry - rz
    elif dy > dz:
        ry = -rx - rz
    else:
        rz = -rx - ry

    return rx, ry, rz


def cube_to_hex(x, y, z):
    return x, y


def hex_to_cube(q, r):
    z = -q - r
    return q, r, z


if __name__ == '__main__':
    gc = GC()
    pc = GolCell(0, 0, 0, gc)
    ph = GolIO(None)
    pv = GolVis(gc, None)
    simulation = ComplexAutomaton(gc, proto_cell=pc, proto_handler=ph, proto_visualizer=pv)
    simulation.run_main_loop()
    # cProfile.run("simulation.run_main_loop()")
