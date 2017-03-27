"""
Main module of the Flow and Pressure Demo.
Uses the Complex Automaton Base.
"""


# External library imports.
import pygame
import math

# CAB system imports.
from cab.abm.cab_agent import CabAgent
from cab.ca.cab_ca_hex import CAHex
from cab.ca.cab_cell import CellHex
from cab.cab_global_constants import GlobalConstants
from cab.cab_system import ComplexAutomaton
from cab.util.cab_input_handling import InputHandler
from cab.util.cab_visualization import Visualization


__author__ = 'Michael Wagner'
__version__ = '1.0'


class GC(GlobalConstants):
    def __init__(self):
        super().__init__()
        self.VERSION = 'version: 09-2014'
        ################################
        #     SIMULATION CONSTANTS     #
        ################################
        self.RUN_SIMULATION = False
        self.ONE_AGENT_PER_CELL = False
        ################################
        #         CA CONSTANTS         #
        ################################
        self.USE_HEX_CA = True
        self.USE_CA_BORDERS = False
        self.DIM_X = 100  # How many cells is the ca wide?
        self.DIM_Y = 100  # How many cells is the ca high?
        self.CELL_SIZE = 7  # How long/wide is one cell?
        self.GRID_WIDTH = self.DIM_X * self.CELL_SIZE
        self.GRID_HEIGHT = self.DIM_Y * self.CELL_SIZE
        ################################
        #        ABM CONSTANTS         #
        ################################
        ################################
        #      UTILITY CONSTANTS       #
        ################################


class SimpleCell(CellHex):
    def __init__(self, x, y, global_const):
        super().__init__(x, y, global_const)
        self.state = False

    def sense_neighborhood(self):
        # for cell in self.neighbors:
        pass

    def update(self):
        pass

    def clone(self, x, y):
        return SimpleCell(x, y, self.gc)


class SimpleAgent(CabAgent):
    def __init__(self, x, y, global_const):
        super().__init__(x, y, global_const)

    def perceive_and_act(self, abm, ca):
        pass


class SimpleIO(InputHandler):
    def __init__(self, cab_sys):
        super().__init__(cab_sys)
        self.dist = 1
        self.show_direction_state = 0
        self.cell_a = None
        self.cell_b = None
        self.cell_c = None
        self.highlighted_cells = []

    def clone(self, cab_sys):
        return SimpleIO(cab_sys)

    def custom_mouse_action(self, button):
        # Click on left mouse button.
        if button == 1:
            # self.add_agent()
            # self.show_neighbors_up_to_dist()
            # self.dist += 1
            self.show_cell_in_direction()
            # self.show_neighbors()
        # Click on middle mouse button / mouse wheel
        elif button == 2:
            self.show_agent_neighborhood()

        # Click on right mouse button
        elif button == 3:
            # self.show_neighbors_up_to_dist()
            # self.dist -= 1
            self.show_agent_empty_neighborhood()

    def show_cell_in_direction(self):
        if self.show_direction_state == 0:
            a_x, a_y = self.get_mouse_hex_coords()
            self.cell_a = self.sys.ca.ca_grid[a_x, a_y]
            self.cell_a.state = True
            self.show_direction_state = 1
        elif self.show_direction_state == 1:
            b_x, b_y = self.get_mouse_hex_coords()
            self.cell_b = self.sys.ca.ca_grid[b_x, b_y]
            self.cell_b.state = True
            self.show_direction_state = 2
            c_x, c_y = CAHex.get_cell_in_direction(self.cell_a, self.cell_b)
            self.cell_c = self.sys.ca.ca_grid[c_x, c_y]
            self.cell_c.state = True
            cube_dist = CAHex.cube_distance(self.cell_a, self.cell_b)
            hex_dist = CAHex.hex_distance(self.cell_a.q, self.cell_a.r, self.cell_b.q, self.cell_b.r)
            print("cube distance between a and b: {0}".format(cube_dist))
            print("hex distance between a and b: {0}".format(hex_dist))
        elif self.show_direction_state == 2:
            self.cell_a.state = False
            self.cell_b.state = False
            self.cell_c.state = False
            self.show_direction_state = 0
        else:
            print('We should never enter this branch!')

    def show_neighbors_up_to_dist(self):
        cell_x, cell_y = self.get_mouse_hex_coords()
        neighborhood = self.sys.ca.get_cell_neighborhood(cell_x, cell_y, self.dist)
        for v in list(self.sys.ca.ca_grid.values()):
            v.state = False
        for v in list(neighborhood.values()):
            v.state = True

    def show_neighbors(self):
        cell_x, cell_y = self.get_mouse_hex_coords()
        print('selected cell: {0}, {1}'.format(cell_x, cell_y))
        for n in self.sys.ca.ca_grid[cell_x, cell_y].neighbors:
            n.state = True

    def add_agent(self):
        agent_x, agent_y = self.get_mouse_hex_coords()
        self.sys.abm.add_agent(SimpleAgent(agent_x, agent_y, self.sys.gc))

    def show_agent_empty_neighborhood(self):
        for cell in self.highlighted_cells:
            cell.state = False
        self.highlighted_cells = []
        agent_x, agent_y = self.get_mouse_hex_coords()
        neighborhood = self.sys.ca.get_empty_agent_neighborhood(agent_x, agent_y, 3)
        for key, value in neighborhood.items():
            self.highlighted_cells.append(value)
            value.state = True

    def show_agent_neighborhood(self):
        for cell in self.highlighted_cells:
            cell.state = False
        self.highlighted_cells = []
        agent_x, agent_y = self.get_mouse_hex_coords()
        agent = self.sys.abm.agent_locations[(agent_x, agent_y)]
        neighborhood = self.sys.ca.get_agent_neighborhood(agent_x, agent_y, agent.vision)
        for key, value in neighborhood.items():
            self.highlighted_cells.append(value[0])
            value[0].state = True


class SimpleVis(Visualization):
    def __init__(self, global_const, sys,  screen):
        super().__init__(global_const, sys, screen)

    def clone(self, cab_sys, screen):
        return SimpleVis(self.gc, cab_sys, screen)

    def draw_cell(self, cell):
        """
        Simple exemplary visualization. Draw cell in white.
        """
        if cell is None:
            pass
        else:
            if cell.state is True:
                pygame.gfxdraw.filled_polygon(self.surface, cell.get_corners(), (200, 0, 55))
            elif cell.state is False and not cell.is_border:
                pygame.gfxdraw.filled_polygon(self.surface, cell.get_corners(), (69, 79, 89))
            elif cell.state is False and cell.is_border:
                pygame.gfxdraw.filled_polygon(self.surface, cell.get_corners(), (89, 79, 69))
            else:
                pygame.gfxdraw.filled_polygon(self.surface, cell.get_corners(), (0, 255, 0))
        pygame.gfxdraw.aapolygon(self.surface, cell.get_corners(), (0, 0, 0))

    def draw_agent(self, agent):
        if agent is None:
            pass
        else:
            radius = int(agent.size / 1.5)

            horiz = self.gc.CELL_SIZE * 2 * (math.sqrt(3) / 2)
            offset = agent.y * (horiz / 2)
            x = int(agent.x * horiz) + int(offset)

            vert = self.gc.CELL_SIZE * 2 * (3 / 4)
            y = int(agent.y * vert)

            pygame.draw.circle(self.surface, (150, 255, 225), (x, y), radius, 0)
            pygame.gfxdraw.aacircle(self.surface, x, y, radius, (50, 100, 50))


if __name__ == '__main__':
    gc = GC()
    pc = SimpleCell(0, 0, gc)
    ph = SimpleIO(None)
    pv = SimpleVis(gc, None, None)
    simulation = ComplexAutomaton(gc, proto_cell=pc, proto_handler=ph, proto_visualizer=pv)
    simulation.run_main_loop()
    # cProfile.run("simulation.run_main_loop()")
