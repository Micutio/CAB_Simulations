"""
Module containing the example cell definition.
"""

# Internal library imports.
from cab.ca.cab_cell import CellHex

__author__ = 'Michael Wagner'
__version__ = '1.0'


class ExampleCell(CellHex):
    """
    This class models one cell of the CA, while the grid itself will be a dictionary of ClassCell instances.
    It inherits from the class CellHex because we declared in the global constants class that this project
    is working with a Cellular Automaton that uses hexagonal cells.
    If instead one wants to use rectangular cells, then ExampleCell has to inherit from CellRect.
    """

    def __init__(self, x, y, gc):
        """
        Initializer method. Usually a cell only needs to know their individual coordinates
        and a reference to the class containing all globally declared constants.
        :param x: X-position of the cell.
        :param y: Y-position of the cell.
        :param gc: Reference to the class containing global constants.
        """
        super().__init__(x, y, gc)
        # Calling the super method initializes the following attributes,
        # which every class that inherits from CabCell and/or CellRect can make use of:
        # self.x = x
        # self.y = y
        # self.gc = gc
        # self.neighbors = []
        # self.rectangular = True
        # self.is_border = False
        # Classes that inherit from CellHex have additional attributes available:
        # self.h = gc.CELL_SIZE * 2
        # self.vert = self.h * (3 / 4)
        # self.w = self.h * (math.sqrt(3) / 2)
        # self.horiz = self.w
        # self.q = x
        # self.r = y
        # self.z = -self.q - self.r
        # self.rectangular = False
        # self.c_size = gc.CELL_SIZE

    def clone(self, x, y):
        """
        The clone method has to be implemented to let the cellular automaton know how to create
        more instances of ExampleCell to fill the grid up with cells.
        :param x: X-position of the cell.
        :param y: Y-position of the cell.
        :return: A new instance of the same class, ExampleCell.
        """
        return ExampleCell(x, y, self.gc)

    def sense_neighborhood(self):
        """
        This method is called at each simulation step to let the cell acquire information about
        its neighboring cells. With this information the cell can then decide whether to change
        its own state. The actual state change however has to be performed within the update()
        method.
        """
        # Example: iterate over all neighboring cells and get information from them.
        # for n in self.neighbors:
        #   do some thing with neighbor n
        pass

    def update(self):
        """
        This method is called at each simulation step, following the sense_neighborhood() method
        to let the cell make changes to its current state. If The information gathered ("sensed")
        in the method sense_neighborhood() warrants any change of this cell's state, then it will
        be performed in this update method, right now.
        """
        pass
