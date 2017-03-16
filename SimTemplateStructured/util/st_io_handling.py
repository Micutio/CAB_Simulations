"""
Module containing the example cell definition.
"""

# External library imports.
import pygame

# CAB system imports.
from cab.util.cab_input_handling import InputHandler

# Internal simulation component imports.
from abm.st_agent import ExampleAgent

__author__ = 'Michael Wagner'
__version__ = '1.0'


class ExampleInputHandler(InputHandler):
    """
    This class handles all user input to the simulation and output back to the user as well.
    """
    def __init__(self, cab_sys):
        super().__init__(cab_sys)

    def clone(self, cab_sys):
        """
        The cloning method only needs to be overridden if the constructor
        requires additional information when called at runtime. (So, almost never.)
        :param cab_sys: Instance of the Complex Automaton System class.
        :return: Initialized instance of ExampleInputHandler
        """
        return ExampleInputHandler(cab_sys)

    def custom_keyboard_action(self, active_key):
        """
        Define customized keyboard actions for this simulation.
        Standard keys like [space], [r] and [s] have already been defined by the system.
        These should not be redefined here anymore!
        :param active_key: Key code of the key that has been pressed.
        """
        if active_key == pygame.K_g:
            self.sys.gc.DISPLAY_GRID = not self.sys.gc.DISPLAY_GRID
            if self.sys.gc.DISPLAY_GRID:
                print('[ss_io_handling] displaying cell grid')
            else:
                print('[ss_io_handling] hiding cell grid')

    def custom_mouse_action(self, button):
        """
        Define customized mouse actions for this simulation.
        This is the place to define what a click on the left/right mouse buttons will do.
        In this example a left click will add another new agent to the cell the mouse is currently hovering over.
        :param button: Numeric code for the pressed mouse button (1 = left, 2 = middle/wheel, 3 = right button)
        """
        # Click on left mouse button.
        # -> set food of cell to max.
        if button == 1:
            agent_x, agent_y = self.get_mouse_hex_coords()
            new_example_agent = ExampleAgent(agent_x, agent_y, self.sys.gc)
            self.sys.abm.add_agent(new_example_agent)
            # Apply changes to abm immediately
            self.sys.abm.schedule_new_agents()
        # Click on right mouse button
        # -> do nothing for now.
        elif button == 3:
            pass
