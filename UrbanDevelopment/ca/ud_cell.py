"""
Module containing the cell definition for the urban world.
"""

from cab.ca.cab_cell import CellHex

__author__ = 'Michael Wagner'
__version__ = '1.0'


class WorldCell(CellHex):
    """
    This class models one cell of the CA, while the grid itself will be a dictionary of ClassCell instances.
    """

    def __init__(self, x, y, gc):
        super().__init__(x, y, gc)
        self.num_neighbors = 0

    def clone(self, x, y):
        return WorldCell(x, y, self.gc)

    def sense_neighborhood(self):
        for n in self.neighbors:
            self.num_neighbors += 1

    def update(self):
        """
        This method regulates the cell's temperature according to the temperature of its neighbors.
        """
        pass