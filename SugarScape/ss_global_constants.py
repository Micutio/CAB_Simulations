__author__ = 'Michael Wagner'
__version__ = '1.0'

from cab.cab_global_constants import GlobalConstants


class GC(GlobalConstants):
    def __init__(self):
        super().__init__()
        self.VERSION = '03-2016'
        self.TITLE = 'Foraging Ant'
        ################################
        #     SIMULATION CONSTANTS     #
        ################################
        self.RUN_SIMULATION = False
        self.TIME_STEP = 0
        self.ONE_AGENT_PER_CELL = True
        ################################
        #        ABM CONSTANTS         #
        ################################
        self.START_AGENTS = 20
        self.VISION = 2
        # self.METABOLISM_SUGAR = 2
        # self.METABOLISM_SPICE = 2
        self.MIN_METABOLISM = 2
        self.MAX_METABOLISM = 6
        self.M_FERTILITY_START = [13, 18]
        self.M_FERTILITY_END = [55, 65]
        self.F_FERTILITY_START = [15, 21]
        self.F_FERTILITY_END = [45, 55]
        self.STARTING_SUGAR = [0, 10]
        self.STARTING_SPICE = [0, 10]
        self.MAX_AGENT_LIFE = 122
        self.IMMUNE_SYSTEM_GENOME_LENGTH = 5
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
        self.MAX_SUGAR = 4
        self.MAX_SPICE = 4
        ################################
        #  SIMULATION SPEC. CONSTANTS  #
        ################################
        self.MAX_ANTS = 25
        self.MAX_PHEROMONE = 100
        self.MAX_FOOD = 100
        self.DIFFUSION = 0.001
        self.EVAPORATION = 0.001
