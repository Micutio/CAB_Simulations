__author__ = 'Michael Wagner'
__version__ = '1.0'

import pygame
import sys
import math

from cab.cab_global_constants import GlobalConstants
from cab.util.cab_input_handling import InputHandler
from abm.ss_agent import SSAgent


class EventHandler(InputHandler):
    def __init__(self, cab_sys):
        super().__init__(cab_sys)

    def clone(self, cab_sys):
        return EventHandler(cab_sys)

    def get_mouse_hex_coords(self):
        _q = (self.mx * math.sqrt(3)/3 - self.my/3)# / self.sys.gc.CELL_SIZE
        _r = self.my * 2/3# / self.sys.gc.CELL_SIZE
        cell_q, cell_r = EventHandler.hex_round(_q, _r)
        return cell_q, cell_r

    def custom_mouse_action(self, button):
        # Click on left mouse button.
        # -> set food of cell to max.
        if button == 1:
            self.show_agent_neighborhood()
        # Click on right mouse button
        # -> toggle cell to be a hive
        # elif button == 3:
        #     self.show_neighbors_up_to_dist()

    def show_neighbors_up_to_dist(self):
        cell_x, cell_y = self.get_mouse_hex_coords()
        agent = self.sys.abm.agent_locations[(cell_x, cell_y)]
        neighborhood = self.sys.ca.get_cell_neighborhood(cell_x, cell_y, agent.vision)
        for v in list(self.sys.ca.ca_grid.values()):
            v.state = False
        for v in list(neighborhood.values()):
            v.state = True

    def show_agent_neighborhood(self):
        agent_x, agent_y = self.get_mouse_hex_coords()
        if(agent_x, agent_y) in self.sys.abm.agent_locations:
            agent = self.sys.abm.agent_locations[(agent_x, agent_y)]
            neighborhood = self.sys.ca.get_empty_agent_neighborhood(agent_x, agent_y, agent.vision)
            for v in list(self.sys.ca.ca_grid.values()):
                v.state = False
            for key, value in neighborhood.items():
                value.state = True

    def custom_keyboard_action(self, active_key):
        if active_key == pygame.K_g:
            self.sys.gc.DISPLAY_GRID = not self.sys.gc.DISPLAY_GRID
            if self.sys.gc.DISPLAY_GRID:
                print('[ss_io_handling] displaying cell grid')
            else:
                print('[ss_io_handling] hiding cell grid')

    @staticmethod
    def hex_round(q, r):
        return EventHandler.cube_to_hex(*EventHandler.cube_round(*EventHandler.hex_to_cube(q, r)))

    @staticmethod
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

    @staticmethod
    def cube_to_hex(x, y, z):
        return x, y

    @staticmethod
    def hex_to_cube(q, r):
        z = -q - r
        return q, r, z