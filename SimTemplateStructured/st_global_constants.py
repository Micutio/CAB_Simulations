from cab.cab_global_constants import GlobalConstants


__author__ = 'Michael Wagner'
__version__ = '1.0'


class ExampleGC(GlobalConstants):
    """
    Class containing constant declarations that are available to all components of the simulation.
    """
    def __init__(self):
        """
        Initializer of the constants class. Nothing else is needed.
        The constants are publicly visible and can be read and written as desired.
        """
        super().__init__()

        # Version number or date
        self.VERSION = '03-2016'
        self.TITLE = 'Example Simulation'

        ################################
        #     SIMULATION CONSTANTS     #
        ################################

        # If true, simulation will start running immediately (without pressing space bar).
        self.RUN_SIMULATION = False
        # Starting time step.
        self.TIME_STEP = 0
        # If True, multiple agents can be on the same cell at the same time, false if not.
        self.ONE_AGENT_PER_CELL = False

        ################################
        #        ABM CONSTANTS         #
        ################################

        # Declare constants that are relevant to the agent model of this simulation.
        
        ################################
        #         CA CONSTANTS         #
        ################################

        # Declare constants that are relevant to the cellular automaton model of this simulation.

        # If True, the CA will use hexagonal cells. If False, the CA will use rectangular cells.
        self.USE_HEX_CA = True
        # If True, the top, left, right and bottom edges of the CA will be hard borders.
        # If False, the cells on one border of the CA will be connected to cells on the opposite border.
        self.USE_CA_BORDERS = True
        # How many cells is the CA wide/high?
        self.DIM_X = 100
        self.DIM_Y = 75
        # How large is the cell diameter in pixels?
        self.CELL_SIZE = 6
        # How wide/high is the CA in pixels?
        self.GRID_WIDTH = self.DIM_X * self.CELL_SIZE
        self.GRID_HEIGHT = self.DIM_Y * self.CELL_SIZE
        # If true, cell borders will be displayed.
        self.DISPLAY_GRID = True

        ################################
        #  SIMULATION SPEC. CONSTANTS  #
        ################################

        # Declare constants that are specific to this simulation, but don't fit into the above categories.
