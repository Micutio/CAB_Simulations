__author__ = 'Michael Wagner'
__version__ = '1.0'

from cab.global_constants import GlobalConstants


class GC(GlobalConstants):
    def __init__(self):
        super().__init__()
        self.VERSION = '03-2016'
        self.TITLE = 'Urban Development simulation'
        self.GUI = "PyGame"  # Options: "None", TK", "PyGame"
        ################################
        #     SIMULATION CONSTANTS     #
        ################################
        self.RUN_SIMULATION = False
        self.TIME_STEP = 0
        self.ONE_AGENT_PER_CELL = False
        self.CELL_VISUAL = "altitude"
        ################################
        #        ABM CONSTANTS         #
        ################################

        ################################
        #         CA CONSTANTS         #
        ################################
        self.USE_HEX_CA = True
        self.USE_CA_BORDERS = True
        self.DIM_X = 75  # How many cells is the ca wide?
        self.DIM_Y = 75  # How many cells is the ca high?
        self.CELL_SIZE = 7
        self.GRID_WIDTH = self.DIM_X * self.CELL_SIZE
        self.GRID_HEIGHT = self.DIM_Y * self.CELL_SIZE
        self.DISPLAY_GRID = False
        ################################
        #  SIMULATION SPEC. CONSTANTS  #
        ################################
