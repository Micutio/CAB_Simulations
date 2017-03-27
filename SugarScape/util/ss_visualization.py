import pygame
import math
from cab.util.cab_visualization import Visualization


__author__ = 'Michael Wagner'
__version__ = '1.0'


class Visualizer(Visualization):
    """
    This class incorporates all methods necessary for visualizing the simulation.
    """

    def __init__(self, gc, surface, sys):
        """
        Initializes the visualization and passes the surface on which to draw.
        :param surface: Pygame surface object.
        """
        # TODO: Comment what the modes do, for better overview.
        super().__init__(gc, surface, sys)
        self.draw_agent_mode = 1
        self.draw_cell_mode = 1
        self.gc = gc

    def clone(self, surface, cab_sys):
        return Visualizer(self.gc, surface, cab_sys)

    def draw_agent(self, agent):
        self.draw_agent_w_color(agent, (180, 180, 180))

    def draw_agent_w_color(self, agent, color):
        # print(agent.x, agent.y)
        if agent.x is not None and agent.y is not None and not agent.dead:
            radius = int(agent.size / 1.5)

            horiz = self.gc.CELL_SIZE * 2 * (math.sqrt(3) / 2)
            offset = agent.y * (horiz / 2)
            x = int(agent.x * horiz) + int(offset)

            vert = self.gc.CELL_SIZE * 2 * (3 / 4)
            y = int(agent.y * vert)
            
            pygame.draw.circle(self.surface, color, (x, y), radius, 0)
            pygame.gfxdraw.aacircle(self.surface, x, y, radius, (50, 100, 50))

    def draw_cell(self, cell):
        """
        Draw cell in following colors:
        a) Dark green if it is a hive.
        b) Yellow if it is food.
        c) According to pheromones there, if it is none of the above.
        :param cell:
        :return:
        """
        red, green, blue = Visualizer.calculate_cell_color(cell, self.gc)
        # print(red, green, blue)
        if cell.state:
            pygame.gfxdraw.filled_polygon(self.surface, cell.corners, (200, 200, 200))
        else:
            pygame.gfxdraw.filled_polygon(self.surface, cell.corners, (red, green, blue))
        if self.gc.DISPLAY_GRID:
            pygame.gfxdraw.aapolygon(self.surface, cell.corners, (190, 190, 190))
        else:
            pygame.gfxdraw.aapolygon(self.surface, cell.corners, (red, green, blue))
        return

    @staticmethod
    def calculate_cell_color(cell, gc):
        if cell.max_sugar == 0:
            normalized_su = 0
        else:
            normalized_su = cell.sugar / gc.MAX_SUGAR
        if cell.max_spice == 0:
            normalized_sp = 0
        else:
            normalized_sp = cell.spice / gc.MAX_SUGAR

        red = int(min(max(0, 150 * normalized_sp), 255))
        green = int(min(max(0, 200 * normalized_su), 255))
        blue = 0
        return red, green, blue
