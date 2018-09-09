"""
Main module of the Flow and Pressure Demo.
Uses the Complex Automaton Base.
"""


# External library imports.
import numpy

# CAB system imports.
import cab.ca.cell as cab_cell
import cab.global_constants as cab_gc
import cab.complex_automaton as cab_sys


__author__ = 'Michael Wagner'
__version__ = '1.0'


class GC(cab_gc.GlobalConstants):
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
        self.USE_MOORE_NEIGHBORHOOD = True
        self.USE_CA_BORDERS = True
        self.DIM_X = 100  # How many cells is the ca wide?
        self.DIM_Y = 100  # How many cells is the ca high?
        self.CELL_SIZE = 7  # How long/wide is one cell?
        self.GRID_WIDTH = self.DIM_X * self.CELL_SIZE
        self.GRID_HEIGHT = self.DIM_Y * self.CELL_SIZE
        self.DISPLAY_GRID = True
        ################################
        #        ABM CONSTANTS         #
        ################################
        ################################
        #      UTILITY CONSTANTS       #
        ################################


class FlowCell(cab_cell.CellHex):
    def __init__(self, x, y, c):
        super().__init__(x, y, c)
        self.pressure = 10
        self.new_pressure = 10
        self.flow = 1
        self.has_color = False
        self.next_color = False
        self.is_solid = False

    def sense_neighborhood(self):
        _pressure = 0
        _neighs = 0
        for cell in self.neighbors:
            if not (cell.is_solid or cell.is_border):
                _pressure += cell.pressure
                _neighs += 1
        if _neighs > 0:
            _pressure /= _neighs
            d_pressure = self.pressure - _pressure
            flow = self.flow * d_pressure
            a = self.pressure / 10.0
            b = -_pressure / 10.0
            if a < b:
                flow = float(numpy.clip(flow, a, b))
            else:
                flow = float(numpy.clip(flow, b, a))
            self.new_pressure -= flow
        # self.flow += flow

    def update(self):
        self.pressure = self.new_pressure
        self.update_cell_color()

    def clone(self, x, y):
        return FlowCell(x, y, self.gc)

    def on_lmb_click(self, abm, ca):
        self.pressure = 50000
        self.update_cell_color()

    def on_rmb_click(self, abm, ca):
        self.pressure = -50000
        self.update_cell_color()

    def update_cell_color(self):
        """
        Simple exemplary visualization. Draw cell in white.
        """
        if self is None:
            pass
        else:
            if self.is_solid:
                self.color = (255, 0, 0)
            elif self.is_border:
                self.color = (150, 190, 100)
            else:
                if self.pressure > 100:
                    red = 255
                    green = 255
                    blue = 255
                elif self.pressure < 0:
                    red = 0
                    green = 0
                    blue = 0
                else:
                    red = int((self.pressure / 100) * 150)
                    green = int((self.pressure / 100) * 150)
                    blue = int((self.pressure / 100) * 255)
                self.color = (red, green, blue)


if __name__ == '__main__':
    gc = GC()
    pc = FlowCell(0, 0, gc)
    simulation = cab_sys.ComplexAutomaton(gc, proto_cell=pc)
    simulation.run_main_loop()
    # cProfile.run("simulation.run_main_loop()")
