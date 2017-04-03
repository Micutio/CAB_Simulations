__author__ = 'Michael Wagner'
__version__ = '1.0'

import pygame
import sys
import math

from cab.cab_global_constants import GlobalConstants
from cab.util.cab_input_handling import InputHandler
from abm.fa_agent import HiveAgent, FoodAgent


class EventHandler(InputHandler):
    def __init__(self, cab_core):
        super().__init__(cab_core)

    def clone(self, cab_core):
        return EventHandler(cab_core)

    def get_mouse_hex_coords(self):
        _q = (self.mx * math.sqrt(3)/3 - self.my/3)  # / self.core.gc.CELL_SIZE
        _r = self.my * 2/3  # / self.core.gc.CELL_SIZE
        cell_q, cell_r = EventHandler.hex_round(_q, _r)
        return cell_q, cell_r

    def custom_keyboard_action(self, active_key):
        if active_key == pygame.K_g:
            self.core.gc.DISPLAY_GRID = not self.core.gc.DISPLAY_GRID
            if self.core.gc.DISPLAY_GRID:
                print('[ss_io_handling] displaying cell grid')
            else:
                print('[ss_io_handling]h iding cell grid')

    def custom_mouse_action(self, button):
        # Click on left mouse button.
        # -> set food of cell to max.
        if button == 1:
            agent_x, agent_y = self.get_mouse_hex_coords()
            food = FoodAgent(agent_x, agent_y, self.core.gc)
            self.core.abm.add_agent(food)
            # Apply changes to abm immediately
            self.core.abm.schedule_new_agents()
        # Click on right mouse button
        # -> toggle cell to be a hive
        elif button == 3:
            agent_x, agent_y = self.get_mouse_hex_coords()
            hive = HiveAgent(agent_x, agent_y, self.core.gc)
            self.core.abm.add_agent(hive)
            # Apply changes to abm immediately
            self.core.abm.schedule_new_agents()
