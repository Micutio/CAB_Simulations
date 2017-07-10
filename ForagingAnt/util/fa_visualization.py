import pygame
import math
from cab.util.cab_visualization import Visualization

from util.fa_io_handling import EventHandler

__author__ = 'Michael Wagner'
__version__ = '1.0'


class Visualizer(Visualization):
    """
    This class incorporates all methods necessary for visualizing the simulation.
    """

    def __init__(self, gc, cab_core):
        """
        Initializes the visualization and passes the surface on which to draw.
        :param cab_core: Reference to the Complex Automaton core class.
        """
        # TODO: Comment what the modes do, for better overview.
        super().__init__(gc, cab_core)
        self.draw_agent_mode = 1
        self.draw_cell_mode = 1
        self.gc = gc
        self.io_handler = EventHandler(cab_core)

    def clone(self, cab_core):
        return Visualizer(self.gc, cab_core)

    def render_simulation(self):
        draw_cell = self.draw_cell
        for c in list(self.ca.ca_grid.values()):
            draw_cell(c)
        draw_agent = self.draw_agent
        for a in self.abm.agent_set:
            draw_agent(a)
        pygame.display.flip()

    def draw_agent(self, agent):
        if agent.id == 'hive':
            self.draw_agent_w_color(agent, (100, 0, 255))
        elif agent.id == 'food':
            self.draw_agent_w_color(agent, (255, 255, 0))
        elif agent.id == 'ant':
            self.draw_agent_w_color(agent, (0, 140, 255))

    def draw_agent_w_color(self, agent, color):
        if agent.x is not None and agent.y is not None and not agent.dead:
            radius = int(agent.size / 1.5)

            horiz = self.gc.CELL_SIZE * 2 * (math.sqrt(3) / 2)
            offset = agent.y * (horiz / 2)
            x = int(agent.x * horiz) + int(offset)

            vert = self.gc.CELL_SIZE * 2 * (3 / 4)
            y = int(agent.y * vert)
            
            pygame.draw.circle(self.surface, color, (x, y), radius, 0)
            pygame.gfxdraw.aacircle(self.surface, x, y, radius, (50, 100, 50))
            # corners = [(x - radius, y - radius),
            #            (x + radius, y - radius),
            #            (x + radius, y + radius),
            #            (x - radius, y + radius),
            #            (x - radius, y - radius)]
            # pygame.gfxdraw.filled_polygon(self.surface, corners, (0, 255, 0))
            # pygame.gfxdraw.aapolygon(self.surface, corners, (0, 100, 0))

            # In case we have an ant, draw its field of vision too.
            # Mostly for debugging purposes.
            # if agent.id == 'ant':
            #     directions = [(1,  0), (1, -1), ( 0, -1), (-1,  0), (-1, 1), ( 0, 1)]
            #     if agent.current_dir == 5:
            #         possible_dirs = [4, 5, 0]
            #     elif agent.current_dir == 0:
            #         possible_dirs = [5, 0, 1]
            #     else:
            #         possible_dirs = [agent.current_dir -1, agent.current_dir, agent.current_dir + 1]
            #     for d in possible_dirs:
            #         try:
            #             cell = self.sys.ca.ca_grid[directions[d][0] + agent.x, directions[d][1] + agent.y]
            #             pygame.gfxdraw.filled_polygon(self.surface, cell.corners, (150, 150, 150))
            #             pygame.gfxdraw.aapolygon(self.surface, cell.corners, (255, 255, 255))
            #         except KeyError:
            #             pass

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
        red = 34  # + int((green + blue) / 2)

        pygame.gfxdraw.filled_polygon(self.surface, cell.corners, (red, green, blue))
        if self.gc.DISPLAY_GRID:
            pygame.gfxdraw.aapolygon(self.surface, cell.corners, (190, 190, 190))
        else:
            pygame.gfxdraw.aapolygon(self.surface, cell.corners, (red, green, blue))
        return
