__author__ = 'Michael Wagner'
__version__ = '1.0'

import pygame
import math
from cab.cab_global_constants import GlobalConstants
from cab.util.cab_visualization import Visualization

class Visualizer(Visualization):
    """
    This class incorporates all methods necessary for visualizing the simulation.
    """

    def __init__(self, gc, screen):
        """
        Initializes the visualization and passes the screen on which to draw.
        :param screen: Pygame screen object.
        """
        # TODO: Comment what the modes do, for better overview.
        super().__init__(gc, screen)
        self.screen = screen
        self.draw_agent_mode = 1
        self.draw_cell_mode = 1
        self.gc = gc

    def clone(self, cab_sys):
        return Visualizer(self.gc, cab_sys)

    def draw_agent(self, agent):
        if agent.id == 'hive':
            self.draw_agent_w_color(agent, (100, 0, 255))
        elif agent.id == 'food':
            self.draw_agent_w_color(agent, (255, 255, 0))
        elif agent.id == 'ant':
            self.draw_agent_w_color(agent, (0, 255, 0))

    def draw_agent_w_color(self, agent, color):
        # print(agent.x, agent.y)
        if agent.x != None and agent.y != None and not agent.dead:
            radius = int(agent.size / 1.5)

            horiz = self.gc.CELL_SIZE * 2 * (math.sqrt(3) / 2)
            offset = agent.y * (horiz / 2)
            x = int(agent.x * horiz) + int(offset)

            vert = self.gc.CELL_SIZE * 2 * (3 / 4)
            y = int(agent.y * vert)
            
            pygame.draw.circle(self.screen, color, (x, y), radius, 0)
            pygame.gfxdraw.aacircle(self.screen, x, y, radius, (50, 100, 50))
            # corners = [(x - radius, y - radius), (x + radius, y - radius), (x + radius, y + radius), (x - radius, y + radius), (x - radius, y - radius)]
            # pygame.gfxdraw.filled_polygon(self.screen, corners, (0, 255, 0))
            # pygame.gfxdraw.aapolygon(self.screen, corners, (0, 100, 0))


    def draw_cell(self, cell):
        """
        Draw cell in following colors:
        a) Dark green if it is a hive.
        b) Yellow if it is food.
        c) According to pheromones there, if it is none of the above.
        :param cell:
        :return:
        """
        green = int(255 * (cell.pheromones["hive"] / self.gc.MAX_PHEROMONE))
        blue = int(255 * (cell.pheromones["food"] / self.gc.MAX_PHEROMONE))
        red = int((green + blue) / 2)

        pygame.gfxdraw.filled_polygon(self.screen, cell.corners, (red, green, blue))
        pygame.gfxdraw.aapolygon(self.screen, cell.corners, (255, 255, 255))

        return