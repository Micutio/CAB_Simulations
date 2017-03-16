"""
Module containing simulation visualization handling.
"""

# External library imports.
import pygame
import math

# Internal simulation component imports.
from cab.util.cab_visualization import Visualization


__author__ = 'Michael Wagner'
__version__ = '1.0'


class ExampleVisualizer(Visualization):
    """
    This class incorporates all methods necessary for visualizing the simulation.
    """

    def __init__(self, gc, surface, sys):
        """
        Initializes the visualization and passes the surface object on which to draw.
        :param surface: Pygame surface object.
        """
        super().__init__(gc, surface, sys)
        self.gc = gc

    def clone(self, surface, cab_sys):
        """
        Cloning method. This needs to be changed only if the Visualizer
        constructor requires additional information at runtime.
        :param surface: Pygame screen object.
        :param cab_sys: Complex Automaton System object.
        :return: Instance of Visualizer class.
        """
        return ExampleVisualizer(self.gc, surface, cab_sys)

    def draw_agent(self, agent):
        """
        Draw an agent onto the cell it currently is located at.
        This method is only applicable to hexagonal cellular automata.
        :param agent: Instance of ExampleAgent
        """
        if agent.x is not None and agent.y is not None and not agent.dead:
            radius = int(agent.size / 1.5)

            horiz = self.gc.CELL_SIZE * 2 * (math.sqrt(3) / 2)
            offset = agent.y * (horiz / 2)
            x = int(agent.x * horiz) + int(offset)

            vert = self.gc.CELL_SIZE * 2 * (3 / 4)
            y = int(agent.y * vert)

            pygame.draw.circle(self.surface, (50, 100, 50), (x, y), radius, 0)
            pygame.gfxdraw.aacircle(self.surface, x, y, radius, (50, 100, 50))

    def draw_cell(self, cell):
        """
        Draw cell in the cellular automaton.
        :param cell: Instance of ExampleCell
        """
        green = 42
        blue = 48
        red = 34

        pygame.gfxdraw.filled_polygon(self.surface, cell.corners, (red, green, blue))
        if self.gc.DISPLAY_GRID:  # Then also draw borders.
            pygame.gfxdraw.aapolygon(self.surface, cell.corners, (190, 190, 190))
        return
