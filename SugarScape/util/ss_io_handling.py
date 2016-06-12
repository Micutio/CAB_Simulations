__author__ = 'Michael Wagner'
__version__ = '1.0'

import pygame
import sys
import math

from cab.cab_global_constants import GlobalConstants
from cab.util.cab_input_handling import InputHandler
from abm.ss_agent import SSAgent


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


class EventHandler(InputHandler):
    def __init__(self, cab_sys):
        super().__init__(cab_sys)

    def clone(self, cab_sys):
        return EventHandler(cab_sys)

    def get_mouse_hex_coords(self):
        _q = (self.mx * math.sqrt(3)/3 - self.my/3)# / self.sys.gc.CELL_SIZE
        _r = self.my * 2/3# / self.sys.gc.CELL_SIZE
        cell_q, cell_r = hex_round(_q, _r)
        return cell_q, cell_r

    def custom_mouse_action(self, button):
        pass
        # Click on left mouse button.
        # -> set food of cell to max.
        # if button == 1:
        #     agent_x, agent_y = self.get_mouse_hex_coords()
        #     food = FoodAgent(agent_x, agent_y, self.sys.gc)
        #     self.sys.abm.add_agent(food)
        # Click on right mouse button
        # -> toggle cell to be a hive
        # elif button == 3:
        #     agent_x, agent_y = self.get_mouse_hex_coords()
        #     hive = HiveAgent(agent_x, agent_y, self.sys.gc)
        #     self.sys.abm.add_agent(hive)

    def custom_keyboard_action(self, active_key):
        if active_key == pygame.K_g:
            self.sys.gc.DISPLAY_GRID = not self.sys.gc.DISPLAY_GRID
            if self.sys.gc.DISPLAY_GRID:
                print('[ss_io_handling] displaying cell grid')
            else:
                print('[ss_io_handling]h iding cell grid')