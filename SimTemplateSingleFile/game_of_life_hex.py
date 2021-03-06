"""
Main module of the Gol and Pressure Demo.
Uses the Complex Automaton Base.
"""

# CAB system imports.
import cab.ca.cell as cab_cell
import cab.global_constants as cab_gc
import cab.complex_automaton as cab_sys


__author__ = 'Michael Wagner'
__version__ = '1.0'


class GC(cab_gc.GlobalConstants):
    def __init__(self):
        super().__init__()
        self.VERSION = 'version: 07-2017'
        self.TITLE = 'Game of Life in hexagonal grid'
        self.GUI = "PyGame"  # Options: "None", TK", "PyGame"
        ################################
        #     SIMULATION CONSTANTS     #
        ################################
        self.RUN_SIMULATION = False
        self.ONE_AGENT_PER_CELL = False
        ################################
        #         CA CONSTANTS         #
        ################################
        self.DISPLAY_GRID = True
        self.USE_HEX_CA = True
        self.USE_MOORE_NEIGHBORHOOD = True
        self.USE_CA_BORDERS = True
        self.DIM_X = 75  # How many cells is the ca wide?
        self.DIM_Y = 75  # How many cells is the ca high?
        self.CELL_SIZE = 7  # How long/wide is one cell?
        self.GRID_WIDTH = self.DIM_X * self.CELL_SIZE
        self.GRID_HEIGHT = self.DIM_Y * self.CELL_SIZE
        ################################
        #        ABM CONSTANTS         #
        ################################
        ################################
        #      UTILITY CONSTANTS       #
        ################################


class GolCell(cab_cell.CellHex):
    def __init__(self, x, y, global_constants):
        super().__init__(x, y, global_constants)
        self.alive = False
        self.next_state = 0
        # The rules:
        #   cell will be [b]orn if it has the following amount of neighbors
        self.b = [2]
        #   cell will [s]tay alive if it has the following amount of neighbors
        self.s = [3, 4]

    def sense_neighborhood(self):
        _neighs_alive = 0
        for cell in self.neighbors:
            if cell.alive and not cell.is_border:
                _neighs_alive += 1

        if not self.alive and _neighs_alive in self.b:
            self.next_state = 1
        elif self.alive and _neighs_alive in self.s:
            self.next_state = 1
        else:
            self.next_state = 0

    def update(self):
        self.alive = self.next_state
        if self.alive:
            self.color = (255, 255, 255)
        else:
            self.color = self.gc.DEFAULT_CELL_COLOR

    def clone(self, x, y):
        return GolCell(x, y, self.gc)

    def on_lmb_click(self, abm, ca):
        self.alive = not self.alive
        if self.alive:
            self.color = (255, 255, 255)
        else:
            self.color = self.gc.DEFAULT_CELL_COLOR

    def on_rmb_click(self, abm, ca):
        self.alive = False
        self.color = self.gc.DEFAULT_CELL_COLOR

if __name__ == '__main__':
    gc = GC()
    pc = GolCell(0, 0, gc)
    simulation = cab_sys.ComplexAutomaton(gc, proto_cell=pc)
    simulation.run_main_loop()

    # Just in case we need to run the simulation in debug mode.
    # cProfile.run("simulation.run_main_loop()")
