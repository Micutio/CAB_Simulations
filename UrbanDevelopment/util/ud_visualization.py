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
        if agent.id == 'hive':
            self.draw_agent_w_color(agent, (100, 0, 255))
        elif agent.id == 'food':
            self.draw_agent_w_color(agent, (255, 255, 0))
        elif agent.id == 'ant':
            self.draw_agent_w_color(agent, (0, 140, 255))

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
        green = 42 + int(213 * (cell.pheromones["hive"] / self.gc.MAX_PHEROMONE))
        blue = 48 + int(207 * (cell.pheromones["food"] / self.gc.MAX_PHEROMONE))
        red = 34 #+ int((green + blue) / 2)

        pygame.gfxdraw.filled_polygon(self.surface, cell.corners, (red, green, blue))
        if self.gc.DISPLAY_GRID:
            pygame.gfxdraw.aapolygon(self.surface, cell.corners, (190, 190, 190))
        else:
            pygame.gfxdraw.aapolygon(self.surface, cell.corners, (red, green, blue))
        return

        return